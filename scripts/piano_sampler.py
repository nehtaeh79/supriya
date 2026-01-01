"""
Render a sampled upright piano riff using the bundled VSCO 2 CE sample pack.

Based on the SuperCollider patch at:
https://pelletierauger.com/en/blog/2020/2/a-piano-for-supercollider.html
"""

from __future__ import annotations

import argparse
import csv
import itertools
import math
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

if sys.version_info < (3, 10):
    raise SystemExit("Python 3.10+ is required to run piano_sampler.py.")

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

try:
    import supriya
except ImportError as exc:  # pragma: no cover - dependency guard
    raise SystemExit(
        "Install supriya in this environment (e.g., `pip install -e .`) before running piano_sampler.py."
    ) from exc
from supriya import Envelope, synthdef
from supriya.ugens import (
    AllpassC,
    Balance2,
    BufDur,
    BufRateScale,
    CombC,
    Dust,
    EnvGen,
    FreeVerb,
    GrainBuf,
    HPF,
    In,
    LFNoise2,
    LeakDC,
    Limiter,
    LPF,
    Out,
    PitchShift,
    PlayBuf,
    SinOsc,
)

SAMPLE_PACK = (
    Path(__file__).with_name("samples")
    / "21055__sgossner__vsco-2-ce-keys-upright-piano"
)
NOTE_RANGE = range(20, 111)
SAMPLES_PER_DYNAMIC = 23
MIN_REALTIME_NODE_BUDGET = 4096


@dataclass
class NoteEvent:
    start: float
    duration: float
    note: int
    velocity: int


@dataclass(frozen=True)
class PerformanceStyle:
    name: str
    description: str
    amp_scale: float = 2.0
    amp_exponent: float = 1.0
    dynamic_curve: float = 1.0
    dynamic_bias: float = 0.0
    attack: float = 0.0
    legato: float = 1.0
    release_scale: float = 0.35
    release_min: float = 0.5
    release_max: float = 4.0
    timing_jitter: float = 0.0
    pan_mode: str = "random"
    pan_jitter: float = 0.0
    melody_gain: float = 1.0
    accompaniment_gain: float = 1.0
    use_fx: bool = False
    fx_wet: float = 0.0
    fx_hp: float = 30.0
    fx_lp_min: float = 800.0
    fx_lp_max: float = 14000.0
    fx_lp_lfo_rate: float = 0.01
    fx_delay_time: float = 0.42
    fx_delay_decay: float = 6.0
    fx_delay_mix: float = 0.2
    fx_reverb_mix: float = 0.4
    fx_room_size: float = 0.9
    fx_damping: float = 0.45
    fx_shimmer_mix: float = 0.0
    fx_shimmer_ratio: float = 1.5
    fx_tail: float = 0.5


PERFORMANCE_STYLES: dict[str, PerformanceStyle] = {
    "raw": PerformanceStyle(
        name="raw",
        description="Direct MIDI playback: dry, per-note random pan, minimal shaping",
    ),
    "debussy": PerformanceStyle(
        name="debussy",
        description="Softer dynamics, more legato, stable keyboard pan, room FX",
        amp_scale=0.3,
        amp_exponent=1.2,
        dynamic_curve=1.3,
        dynamic_bias=-0.15,
        attack=0.008,
        legato=1.05,
        release_scale=0.65,
        release_min=2.5,
        release_max=12.0,
        timing_jitter=0.004,
        pan_mode="keyboard",
        pan_jitter=0.045,
        melody_gain=1.06,
        accompaniment_gain=0.88,
        use_fx=True,
        fx_wet=0.92,
        fx_hp=28.0,
        fx_lp_min=700.0,
        fx_lp_max=14000.0,
        fx_lp_lfo_rate=0.01,
        fx_delay_time=0.43,
        fx_delay_decay=6.0,
        fx_delay_mix=0.2,
        fx_reverb_mix=0.38,
        fx_room_size=0.92,
        fx_damping=0.45,
        fx_shimmer_mix=0.0,
        fx_shimmer_ratio=1.5,
        fx_tail=10.0,
    ),
}


def midiratio(semitones: float) -> float:
    return 2 ** (semitones / 12)


def make_lookup(note: int, dynamic: int) -> tuple[int, int]:
    octave = math.floor(note / 12) - 2
    degree = note % 12
    sampled_note = [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3]
    note_deltas = [-1, 0, 1, 2, -1, 0, 1, -2, -1, 0, 1, 2]
    dynamic_offset = dynamic * SAMPLES_PER_DYNAMIC
    sample_to_get = octave * 3 + sampled_note[degree] + dynamic_offset
    pitch = note_deltas[degree]
    return sample_to_get, pitch


def build_lookup(quiet: bool) -> tuple[list[int], list[int], int]:
    dynamic_count = 2 if quiet else 3
    max_dynamic = 1 if quiet else 2
    indices: list[int] = []
    pitches: list[int] = []
    for dynamic in range(dynamic_count):
        for note in NOTE_RANGE:
            sample_index, pitch = make_lookup(note, dynamic)
            indices.append(sample_index)
            pitches.append(pitch)
    return indices, pitches, max_dynamic


def clamp_note_and_dynamic(note: float, dynamic: float, max_dynamic: int) -> tuple[float, int]:
    clamped_note = max(min(note, NOTE_RANGE.stop - 1), NOTE_RANGE.start)
    clamped_dynamic = int(max(min(math.floor(dynamic), max_dynamic), 0))
    return clamped_note, clamped_dynamic


def select_sample(
    note: float,
    dynamic: float,
    indices: list[int],
    pitches: list[int],
    max_dynamic: int,
) -> tuple[int, float]:
    clamped_note, clamped_dynamic = clamp_note_and_dynamic(note, dynamic, max_dynamic)
    note_floor = math.floor(clamped_note)
    index = note_floor - NOTE_RANGE.start + (clamped_dynamic * len(NOTE_RANGE))
    sample_index = indices[index]
    pitch = pitches[index]
    rate = midiratio(pitch + (clamped_note - note_floor))
    return sample_index, rate


def iter_pattern(values: list[float] | list[int]) -> itertools.cycle:
    return itertools.cycle(values)


def schedule_pattern(
    context: supriya.Context,
    buffers: list[supriya.Buffer],
    indices: list[int],
    pitches: list[int],
    max_dynamic: int,
    *,
    start_time: float,
    duration: float,
    notes: list[int],
    durs: list[float],
    dynamics: list[int],
    amps: list[float],
    rel: float,
    pan_range: tuple[float, float],
    rng: random.Random,
) -> float:
    base_time = 0.0 if isinstance(context, supriya.Score) else time.time()
    note_iter = iter_pattern(notes)
    dur_iter = iter_pattern(durs)
    dyn_iter = iter_pattern(dynamics)
    amp_iter = iter_pattern(amps)
    current_time = start_time
    while current_time < start_time + duration:
        note = float(next(note_iter))
        dur = float(next(dur_iter))
        dyn = float(next(dyn_iter))
        amp = float(next(amp_iter))
        pan = rng.uniform(*pan_range)
        sample_index, rate = select_sample(note, dyn, indices, pitches, max_dynamic)
        buffer = buffers[sample_index]
        with context.at(base_time + current_time):
            context.add_synth(
                piano_synth,
                buf=buffer,
                rate=rate,
                pan=pan,
                amp=amp,
                rel=rel,
            )
        current_time += dur
    return start_time + duration + rel


@synthdef()
def piano_synth(
    buf=0,
    rate=1,
    spos=0,
    pan=0,
    amp=1,
    out=0,
    atk=0,
    sus=0,
    rel=8,
):
    env = EnvGen.kr(
        envelope=Envelope([0, 1, 1, 0], [atk, sus, rel]),
        done_action=2,
    )
    sig = PlayBuf.ar(
        buffer_id=buf,
        channel_count=2,
        rate=rate * BufRateScale.ir(buffer_id=buf),
        start_position=spos,
        done_action=2,
    )
    sig = sig * amp * 18 * env
    sig = Balance2.ar(left=sig[0], right=sig[1], position=pan, level=1)
    Out.ar(bus=out, source=sig)


@synthdef()
def piano_synth_room(
    buf=0,
    rate=1,
    spos=0,
    pan=0,
    amp=1,
    out=0,
    atk=0.0,
    sus=0.0,
    rel=8.0,
    hp=25.0,
    lp=18000.0,
    reverb_mix=0.35,
    room_size=0.9,
    damping=0.45,
):
    env = EnvGen.kr(
        envelope=Envelope([0, 1, 1, 0], [atk, sus, rel]),
        done_action=2,
    )
    sig = PlayBuf.ar(
        buffer_id=buf,
        channel_count=2,
        rate=rate * BufRateScale.ir(buffer_id=buf),
        start_position=spos,
        done_action=2,
    )
    sig = [
        LPF.ar(
            source=HPF.ar(source=LeakDC.ar(source=sig[i]), frequency=hp),
            frequency=lp,
        )
        for i in range(2)
    ]
    sig = [x * amp * 18 * env for x in sig]
    sig = Balance2.ar(left=sig[0], right=sig[1], position=pan, level=1)
    reverbed = [
        FreeVerb.ar(
            source=sig[ch],
            mix=reverb_mix,
            room_size=room_size,
            damping=damping,
        )
        for ch in range(2)
    ]
    Out.ar(bus=out, source=reverbed)


@synthdef()
def ambient_piano_gesture(
    buf=0,
    rate=1,
    spos=0,
    pan=0,
    amp=1,
    out=0,
    atk=0.005,
    sus=0,
    rel=10,
    hp=25.0,
    lp=18000.0,
):
    env = EnvGen.kr(
        envelope=Envelope([0, 1, 1, 0], [atk, sus, rel]),
        done_action=2,
    )
    sig = PlayBuf.ar(
        buffer_id=buf,
        channel_count=2,
        rate=rate * BufRateScale.ir(buffer_id=buf),
        start_position=spos,
        done_action=0,
    )
    sig = [
        LPF.ar(
            source=HPF.ar(source=LeakDC.ar(source=sig[i]), frequency=hp),
            frequency=lp,
        )
        for i in range(2)
    ]
    sig = [x * amp * 18 * env for x in sig]
    sig = Balance2.ar(left=sig[0], right=sig[1], position=pan, level=1)
    Out.ar(bus=out, source=sig)


@synthdef()
def ambient_piano_grain_cloud(
    buffer_id=0,
    out=0,
    amp=0.1,
    amp_lag=4.0,
    pan=0.0,
    pan_spread=0.35,
    density=3.0,
    density_lag=2.5,
    base_grain_duration=0.15,
    grain_duration_jitter=0.08,
    base_rate=1.0,
    rate_lag=4.0,
    pitch_mod_semitones=0.0,
    position_mod_rate=0.07,
    position_min=0.1,
    position_max=0.85,
    filter_min=80.0,
    filter_max=8000.0,
    filter_mod_rate=0.03,
):
    amp_ = supriya.ugens.Lag.kr(source=amp, lag_time=amp_lag)
    density_ = supriya.ugens.Lag.kr(source=density, lag_time=density_lag)
    base_rate_ = supriya.ugens.Lag.kr(source=base_rate, lag_time=rate_lag)
    density_lfo = 0.65 + 0.35 * (
        (LFNoise2.kr(frequency=position_mod_rate * 0.11) + 1) * 0.5
    )
    trig = Dust.kr(density=density_ * density_lfo)
    buffer_duration = BufDur.kr(buffer_id=buffer_id)
    position_lfo = (LFNoise2.kr(frequency=position_mod_rate) + 1) * 0.5
    position = (
        (position_min + position_lfo * (position_max - position_min)) * buffer_duration
    )
    duration_noise = (LFNoise2.kr(frequency=position_mod_rate * 0.617) + 1) * 0.5
    grain_duration = base_grain_duration + (duration_noise * grain_duration_jitter)
    pitch_noise = LFNoise2.kr(frequency=position_mod_rate * 0.431)
    pitch_ratio = 2 ** ((pitch_noise * pitch_mod_semitones) / 12)
    rate = base_rate_ * pitch_ratio * BufRateScale.kr(buffer_id=buffer_id)
    pan_mod = pan + (LFNoise2.kr(frequency=position_mod_rate * 0.2) * pan_spread)
    grains = GrainBuf.ar(
        channel_count=2,
        trigger=trig,
        duration=grain_duration,
        buffer_id=buffer_id,
        rate=rate,
        position=position,
        interpolate=2,
        pan=pan_mod,
        envelope_buffer_id=-1,
        maximum_overlap=256,
    )
    cutoff_noise = (LFNoise2.kr(frequency=filter_mod_rate) + 1) * 0.5
    cutoff = filter_min + cutoff_noise * (filter_max - filter_min)
    filtered = [
        HPF.ar(
            source=LPF.ar(source=LeakDC.ar(source=grains[i]), frequency=cutoff),
            frequency=20,
        )
        for i in range(2)
    ]
    amp_lfo = 0.7 + 0.3 * (
        (SinOsc.kr(frequency=position_mod_rate * 0.13) + 1) * 0.5
    )
    Out.ar(bus=out, source=[x * amp_ * amp_lfo for x in filtered])


@synthdef()
def ambient_piano_master_fx(
    in_bus=0,
    out=0,
    wet=0.9,
    hp=30.0,
    lp_min=800.0,
    lp_max=14000.0,
    lp_lfo_rate=0.01,
    delay_time=0.42,
    delay_decay=6.0,
    delay_mix=0.2,
    reverb_mix=0.4,
    room_size=0.9,
    damping=0.45,
    shimmer_mix=0.08,
    shimmer_ratio=1.5,
):
    source = In.ar(bus=in_bus, channel_count=2)
    lfo = (SinOsc.kr(frequency=lp_lfo_rate) + 1) * 0.5
    cutoff = lp_min + lfo * (lp_max - lp_min)
    shaped = [
        LPF.ar(
            source=HPF.ar(source=LeakDC.ar(source=source[i]), frequency=hp),
            frequency=cutoff,
        )
        for i in range(2)
    ]
    diffused = shaped
    for i, base_delay in enumerate((0.031, 0.047, 0.059)):
        mod = SinOsc.kr(frequency=0.02 + (i * 0.01)) * 0.005
        diffused = [
            AllpassC.ar(
                source=diffused[ch],
                maximum_delay_time=0.2,
                delay_time=base_delay + mod,
                decay_time=3.0 + (i * 1.5),
            )
            for ch in range(2)
        ]
    echo_time = delay_time * (0.7 + 0.3 * ((LFNoise2.kr(frequency=0.03) + 1) * 0.5))
    echo = [
        CombC.ar(
            source=diffused[ch],
            maximum_delay_time=1.0,
            delay_time=echo_time,
            decay_time=delay_decay,
        )
        for ch in range(2)
    ]
    pre_reverb = [diffused[ch] + (echo[ch] * delay_mix) for ch in range(2)]
    reverbed = [
        FreeVerb.ar(
            source=pre_reverb[ch],
            mix=reverb_mix,
            room_size=room_size,
            damping=damping,
        )
        for ch in range(2)
    ]
    shimmered = [
        PitchShift.ar(
            source=reverbed[ch],
            window_size=0.2,
            pitch_ratio=shimmer_ratio,
            pitch_dispersion=0.02,
            time_dispersion=0.02,
        )
        for ch in range(2)
    ]
    wet_signal = [
        (reverbed[ch] * (1 - shimmer_mix)) + (shimmered[ch] * shimmer_mix)
        for ch in range(2)
    ]
    mixed = [(shaped[ch] * (1 - wet)) + (wet_signal[ch] * wet) for ch in range(2)]
    limited = [
        Limiter.ar(source=LeakDC.ar(source=mixed[ch]), level=0.95, duration=0.01)
        for ch in range(2)
    ]
    Out.ar(bus=out, source=limited)


def load_sample_buffers(
    context: supriya.Context, sample_pack: Path
) -> list[supriya.Buffer]:
    if not sample_pack.exists():
        raise FileNotFoundError(f"Sample pack not found: {sample_pack}")
    sample_paths = sorted(sample_pack.glob("*.wav"))
    if not sample_paths:
        raise FileNotFoundError(f"No wav files found in {sample_pack}")
    buffers: list[supriya.Buffer] = []
    if isinstance(context, supriya.Score):
        with context.at(0):
            context.add_synthdefs(piano_synth)
            context.add_synthdefs(piano_synth_room)
            for path in sample_paths:
                buffers.append(context.add_buffer(file_path=path))
        return buffers

    context.add_synthdefs(piano_synth)
    context.add_synthdefs(piano_synth_room)
    for path in sample_paths:
        buffers.append(context.add_buffer(file_path=path))
    return buffers


def velocity_to_dynamic(
    velocity: int,
    max_dynamic: int,
    *,
    curve: float = 1.0,
    bias: float = 0.0,
) -> int:
    if max_dynamic <= 0:
        return 0
    clamped_velocity = max(0, min(int(velocity), 127))
    normalized = (clamped_velocity / 127.0) ** max(0.0001, float(curve))
    dynamic = int(round((normalized * max_dynamic) + float(bias)))
    return max(0, min(dynamic, max_dynamic))


def parse_midi_file(path: Path) -> list[NoteEvent]:
    try:
        import mido
    except ImportError as exc:
        raise RuntimeError(
            "Parsing .mid files requires the 'mido' package. Install it with pip."
        ) from exc
    midi = mido.MidiFile(path)
    tempo = 500000
    ticks_per_beat = midi.ticks_per_beat
    events: list[NoteEvent] = []
    active: dict[tuple[int, int], list[tuple[float, int]]] = {}
    current_time = 0.0
    for message in mido.merge_tracks(midi.tracks):
        current_time += mido.tick2second(message.time, ticks_per_beat, tempo)
        if message.type == "set_tempo":
            tempo = message.tempo
            continue
        if message.type == "note_on" and message.velocity > 0:
            active.setdefault((message.channel, message.note), []).append(
                (current_time, message.velocity)
            )
        elif message.type in ("note_off", "note_on"):
            stack = active.get((message.channel, message.note))
            if not stack:
                continue
            start_time, velocity = stack.pop(0)
            duration = max(0.0, current_time - start_time)
            events.append(
                NoteEvent(
                    start=start_time,
                    duration=duration,
                    note=message.note,
                    velocity=velocity,
                )
            )
    return events


def parse_midicsv_file(path: Path) -> list[NoteEvent]:
    rows: list[tuple[int, int, list[str]]] = []
    ticks_per_beat: int | None = None
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.reader(handle, skipinitialspace=True)
        for index, row in enumerate(reader):
            if not row:
                continue
            try:
                tick = int(row[1])
            except (IndexError, ValueError):
                continue
            event = row[2].strip() if len(row) > 2 else ""
            if event == "Header":
                try:
                    ticks_per_beat = int(row[5])
                except (IndexError, ValueError):
                    continue
            rows.append((tick, index, row))
    if ticks_per_beat is None:
        raise ValueError(f"Missing Header division in {path}")
    tempo = 500000
    events: list[NoteEvent] = []
    active: dict[tuple[int, int], list[tuple[float, int]]] = {}
    rows.sort(key=lambda item: (item[0], item[1]))
    current_time = 0.0
    last_tick = 0
    for tick, _, row in rows:
        if tick > last_tick:
            delta_ticks = tick - last_tick
            current_time += (delta_ticks * tempo) / (ticks_per_beat * 1_000_000)
            last_tick = tick
        event = row[2].strip() if len(row) > 2 else ""
        if event == "Tempo":
            try:
                tempo = int(row[3])
            except (IndexError, ValueError):
                continue
        elif event in ("Note_on_c", "Note_off_c"):
            try:
                note = int(row[4])
                velocity = int(row[5])
            except (IndexError, ValueError):
                continue
            if event == "Note_on_c" and velocity > 0:
                channel = int(row[3])
                active.setdefault((channel, note), []).append((current_time, velocity))
            else:
                channel = int(row[3])
                stack = active.get((channel, note))
                if not stack:
                    continue
                start_time, start_velocity = stack.pop(0)
                duration = max(0.0, current_time - start_time)
                events.append(
                    NoteEvent(
                        start=start_time,
                        duration=duration,
                        note=note,
                        velocity=start_velocity,
                    )
                )
    return events


def load_note_events(path: Path) -> list[NoteEvent]:
    suffix = path.suffix.lower()
    if suffix in (".mid", ".midi"):
        return parse_midi_file(path)
    if suffix in (".csv", ".midicsv"):
        return parse_midicsv_file(path)
    raise ValueError(f"Unsupported MIDI file extension: {path.suffix}")


def schedule_note_events(
    context: supriya.Context,
    buffers: list[supriya.Buffer],
    indices: list[int],
    pitches: list[int],
    max_dynamic: int,
    events: list[NoteEvent],
    *,
    start_time: float,
    pan_range: tuple[float, float],
    rng: random.Random,
    performance: PerformanceStyle | None = None,
    out: int | supriya.BusGroup = 0,
    target_node: supriya.Node | None = None,
) -> float:
    performance_ = PERFORMANCE_STYLES["raw"] if performance is None else performance
    voice_synthdef = piano_synth_room if performance_.use_fx else piano_synth
    max_end_time = start_time
    base_time = 0.0 if isinstance(context, supriya.Score) else time.time()
    sorted_events = sorted(events, key=lambda e: e.start)
    for _, group in itertools.groupby(sorted_events, key=lambda e: e.start):
        group_events = list(group)
        top_note = max(event.note for event in group_events)
        for event in group_events:
            dynamic = velocity_to_dynamic(
                event.velocity,
                max_dynamic,
                curve=performance_.dynamic_curve,
                bias=performance_.dynamic_bias,
            )
            sample_index, rate = select_sample(
                float(event.note),
                float(dynamic),
                indices,
                pitches,
                max_dynamic,
            )
            buffer = buffers[sample_index]
            if performance_.pan_mode == "keyboard":
                pan = _note_to_pan(event.note, pan_range=pan_range)
                if performance_.pan_jitter:
                    pan += rng.uniform(-performance_.pan_jitter, performance_.pan_jitter)
                pan = max(pan_range[0], min(pan_range[1], pan))
            else:
                pan = rng.uniform(*pan_range)
            amplitude = supriya.conversions.midi_velocity_to_amplitude(event.velocity)
            amplitude = (amplitude**performance_.amp_exponent) * performance_.amp_scale
            if event.note == top_note:
                amplitude *= performance_.melody_gain
            else:
                amplitude *= performance_.accompaniment_gain
            release = max(
                float(performance_.release_min),
                min(float(performance_.release_max), event.duration * performance_.release_scale),
            )
            sustain = max(0.0, event.duration * performance_.legato)
            note_start = start_time + event.start
            if performance_.timing_jitter:
                note_start += rng.uniform(
                    -performance_.timing_jitter, performance_.timing_jitter
                )
                note_start = max(start_time, note_start)
            with context.at(base_time + note_start):
                add_synth_kwargs: dict[str, object] = {
                    "buf": buffer,
                    "rate": rate,
                    "pan": pan,
                    "amp": amplitude,
                    "atk": performance_.attack,
                    "sus": sustain,
                    "rel": release,
                    "out": out,
                }
                if voice_synthdef is piano_synth_room:
                    reverb_mix = float(performance_.fx_wet) * float(
                        performance_.fx_reverb_mix
                    )
                    reverb_mix = max(0.0, min(1.0, reverb_mix))
                    add_synth_kwargs.update(
                        hp=float(performance_.fx_hp),
                        lp=float(performance_.fx_lp_max),
                        reverb_mix=reverb_mix,
                        room_size=float(performance_.fx_room_size),
                        damping=float(performance_.fx_damping),
                    )
                if target_node is not None:
                    add_synth_kwargs["target_node"] = target_node
                    add_synth_kwargs["add_action"] = "ADD_TO_HEAD"
                context.add_synth(voice_synthdef, **add_synth_kwargs)
            max_end_time = max(
                max_end_time,
                note_start + performance_.attack + sustain + release,
            )
    return max_end_time


def schedule_riff(
    context: supriya.Context,
    buffers: list[supriya.Buffer],
    indices: list[int],
    pitches: list[int],
    max_dynamic: int,
    *,
    duration: float,
    seed: int,
) -> float:
    rng = random.Random(seed)
    riff_start = 0.1
    tail = schedule_pattern(
        context,
        buffers,
        indices,
        pitches,
        max_dynamic,
        start_time=riff_start,
        duration=duration,
        notes=[62, 65, 69, 72, 57, 64, 65, 71],
        durs=[0.5, 0.25, 0.25, 0.25],
        dynamics=[1, 0, 0, 1],
        amps=[0.5, 2, 2, 0.5],
        rel=4,
        pan_range=(-0.75, 0.75),
        rng=rng,
    )
    tail = max(
        tail,
        schedule_pattern(
            context,
            buffers,
            indices,
            pitches,
            max_dynamic,
            start_time=riff_start,
            duration=duration,
            notes=[100, 93, 98, 96],
            durs=[0.25, 1.75],
            dynamics=[1, 1, 1, 1],
            amps=[0.5, 1, 1, 0.5],
            rel=4,
            pan_range=(-0.75, 0.75),
            rng=rng,
        ),
    )
    return tail


def render_score(
    score: supriya.Score,
    *,
    output_path: Path,
    end_time: float,
) -> tuple[Path | None, int]:
    with score.at(end_time):
        score.do_nothing()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return supriya.render(score, output_file_path=output_path, header_format="wav")


def render_riff(
    output_path: Path,
    *,
    duration: float,
    quiet: bool,
    seed: int,
) -> tuple[Path | None, int]:
    score = supriya.Score(output_bus_channel_count=2)
    buffers = load_sample_buffers(score, SAMPLE_PACK)
    indices, pitches, max_dynamic = build_lookup(quiet=quiet)
    end_time = schedule_riff(
        score,
        buffers,
        indices,
        pitches,
        max_dynamic,
        duration=duration,
        seed=seed,
    )
    return render_score(score, output_path=output_path, end_time=end_time)


def render_midi(
    output_path: Path,
    *,
    events: list[NoteEvent],
    quiet: bool,
    seed: int,
    performance: PerformanceStyle,
) -> tuple[Path | None, int]:
    score = supriya.Score(output_bus_channel_count=2)
    buffers = load_sample_buffers(score, SAMPLE_PACK)
    indices, pitches, max_dynamic = build_lookup(quiet=quiet)
    rng = random.Random(seed)
    end_time = schedule_note_events(
        score,
        buffers,
        indices,
        pitches,
        max_dynamic,
        events,
        start_time=0.1,
        pan_range=(-0.75, 0.75),
        rng=rng,
        performance=performance,
    )
    return render_score(score, output_path=output_path, end_time=end_time + 0.5)


def realtime_options(expected_nodes: int, *, sample_rate: int | None = None) -> supriya.Options:
    node_budget = max(MIN_REALTIME_NODE_BUDGET, expected_nodes * 4)
    if sample_rate is None:
        return supriya.Options(maximum_node_count=node_budget)
    return supriya.Options(maximum_node_count=node_budget, sample_rate=sample_rate)


def play_midi(
    *,
    events: list[NoteEvent],
    quiet: bool,
    seed: int,
    performance: PerformanceStyle,
) -> None:
    server = supriya.Server(options=realtime_options(len(events))).boot()
    buffers = load_sample_buffers(server, SAMPLE_PACK)
    tail = 0.5
    server.sync()
    indices, pitches, max_dynamic = build_lookup(quiet=quiet)
    rng = random.Random(seed)
    end_time = schedule_note_events(
        server,
        buffers,
        indices,
        pitches,
        max_dynamic,
        events,
        start_time=0.1,
        pan_range=(-0.75, 0.75),
        rng=rng,
        performance=performance,
    )
    time.sleep(end_time + tail)
    server.quit()


def play_riff(
    *,
    duration: float,
    quiet: bool,
    seed: int,
) -> None:
    server = supriya.Server(options=realtime_options(int(duration * 16))).boot()
    buffers = load_sample_buffers(server, SAMPLE_PACK)
    server.sync()
    indices, pitches, max_dynamic = build_lookup(quiet=quiet)
    end_time = schedule_riff(
        server,
        buffers,
        indices,
        pitches,
        max_dynamic,
        duration=duration,
        seed=seed,
    )
    time.sleep(end_time + 0.5)
    server.quit()


@dataclass(frozen=True)
class Program:
    name: str
    description: str
    runner: Callable[[argparse.Namespace], None] | None = None

    @property
    def implemented(self) -> bool:
        return self.runner is not None


AMBIENT_01_CHORDS: list[list[int]] = [
    [48, 55, 64, 71, 74],  # Cmaj9
    [45, 52, 60, 67, 71],  # Am9
    [41, 48, 57, 64, 67],  # Fmaj9
    [43, 50, 59, 62, 69],  # G6/9
]
BACKGROUND_01_SCALE_OFFSETS = [0, 2, 3, 5, 7, 9, 10]  # D Dorian
BACKGROUND_01_ROOT = 62


def _note_to_pan(note: int, *, pan_range: tuple[float, float] = (-0.75, 0.75)) -> float:
    position = (note - NOTE_RANGE.start) / (NOTE_RANGE.stop - NOTE_RANGE.start - 1)
    return pan_range[0] + position * (pan_range[1] - pan_range[0])


def _build_scale_notes(
    root: int,
    scale_offsets: list[int],
    *,
    low: int,
    high: int,
) -> list[int]:
    if low > high:
        raise ValueError("low must be <= high")
    root_pc = root % 12
    pitch_classes = {(root_pc + offset) % 12 for offset in scale_offsets}
    return [note for note in range(low, high + 1) if note % 12 in pitch_classes]


def _euclidean_pattern(pulses: int, steps: int) -> list[int]:
    if steps <= 0:
        return []
    pulses = max(0, min(pulses, steps))
    if pulses == 0:
        return [0] * steps
    if pulses == steps:
        return [1] * steps
    return [1 if (i * pulses) % steps < pulses else 0 for i in range(steps)]


def _build_scale_chord(scale_notes: list[int], root_index: int) -> list[int]:
    chord_intervals = (0, 2, 4, 6)
    max_root = max(0, len(scale_notes) - chord_intervals[-1] - 1)
    safe_root = max(0, min(root_index, max_root))
    return [scale_notes[safe_root + interval] for interval in chord_intervals]


def _schedule_background_note(
    server: supriya.Server,
    *,
    buffers: list[supriya.Buffer],
    indices: list[int],
    pitches: list[int],
    max_dynamic: int,
    note: int,
    velocity: int,
    start_time: float,
    duration: float,
    performance: PerformanceStyle,
    out_bus: supriya.BusGroup,
    rng: random.Random,
) -> None:
    dynamic = velocity_to_dynamic(
        velocity,
        max_dynamic,
        curve=performance.dynamic_curve,
        bias=performance.dynamic_bias,
    )
    sample_index, rate = select_sample(
        float(note), float(dynamic), indices, pitches, max_dynamic
    )
    buffer = buffers[sample_index]
    pan = _note_to_pan(note)
    if performance.pan_jitter:
        pan += rng.uniform(-performance.pan_jitter, performance.pan_jitter)
    pan = max(-0.95, min(0.95, pan))
    amplitude = supriya.conversions.midi_velocity_to_amplitude(velocity)
    amplitude = (amplitude**performance.amp_exponent) * performance.amp_scale
    sustain = max(0.0, duration * performance.legato)
    release = max(
        float(performance.release_min),
        min(float(performance.release_max), duration * performance.release_scale),
    )
    atk = float(performance.attack)
    note_time = max(start_time, time.time())
    reverb_mix = float(performance.fx_wet) * float(performance.fx_reverb_mix)
    reverb_mix = max(0.0, min(1.0, reverb_mix))
    with server.at(note_time):
        server.add_synth(
            piano_synth_room,
            buf=buffer,
            rate=rate,
            pan=pan,
            amp=amplitude,
            atk=atk,
            sus=sustain,
            rel=release,
            out=out_bus,
            hp=float(performance.fx_hp),
            lp=float(performance.fx_lp_max),
            reverb_mix=reverb_mix,
            room_size=float(performance.fx_room_size),
            damping=float(performance.fx_damping),
        )


def _spawn_ambient_clouds(
    server: supriya.Server,
    *,
    buffers: list[supriya.Buffer],
    indices: list[int],
    pitches: list[int],
    max_dynamic: int,
    chord_notes: list[int],
    target_node: supriya.Node,
    out_bus: supriya.BusGroup,
    intensity: float,
    rng: random.Random,
    fade_time: float,
) -> list[supriya.Synth]:
    density_scale = 0.55 + (intensity * 1.35)
    amp_scale = 0.7 + (intensity * 0.8)
    clouds: list[supriya.Synth] = []
    for i, note in enumerate(chord_notes):
        register = (note - NOTE_RANGE.start) / (NOTE_RANGE.stop - NOTE_RANGE.start - 1)
        if register < 0.33:
            base_density = 0.65
            base_grain_duration = 0.35
            grain_duration_jitter = 0.2
            pitch_mod_semitones = 0.35
            filter_min, filter_max = 35.0, 1200.0
            base_amp = 0.06
        elif register < 0.66:
            base_density = 1.6
            base_grain_duration = 0.22
            grain_duration_jitter = 0.14
            pitch_mod_semitones = 0.75
            filter_min, filter_max = 90.0, 6000.0
            base_amp = 0.045
        else:
            base_density = 2.8
            base_grain_duration = 0.14
            grain_duration_jitter = 0.1
            pitch_mod_semitones = 1.75
            filter_min, filter_max = 220.0, 11000.0
            base_amp = 0.035
        dynamic = 0 if rng.random() < 0.85 else min(1, max_dynamic)
        sample_index, rate = select_sample(
            float(note), float(dynamic), indices, pitches, max_dynamic
        )
        buffer = buffers[sample_index]
        detune = rng.uniform(0.997, 1.003)
        pan = _note_to_pan(note) + rng.uniform(-0.05, 0.05)
        position_mod_rate = rng.uniform(0.02, 0.08)
        filter_mod_rate = rng.uniform(0.01, 0.05)
        synth = server.add_synth(
            ambient_piano_grain_cloud,
            target_node=target_node,
            add_action="ADD_TO_HEAD",
            buffer_id=buffer,
            out=out_bus,
            amp=0.0,
            amp_lag=fade_time,
            pan=pan,
            pan_spread=0.25,
            density=base_density * density_scale,
            base_grain_duration=base_grain_duration,
            grain_duration_jitter=grain_duration_jitter,
            base_rate=rate * detune,
            pitch_mod_semitones=pitch_mod_semitones,
            position_mod_rate=position_mod_rate,
            filter_min=filter_min,
            filter_max=filter_max,
            filter_mod_rate=filter_mod_rate,
        )
        synth.set(amp=base_amp * amp_scale)
        clouds.append(synth)
    return clouds


def _trigger_ambient_gesture(
    server: supriya.Server,
    *,
    buffers: list[supriya.Buffer],
    indices: list[int],
    pitches: list[int],
    max_dynamic: int,
    chord_notes: list[int],
    out_bus: supriya.BusGroup,
    intensity: float,
    rng: random.Random,
    accent: bool = False,
) -> None:
    candidates: set[int] = set(chord_notes)
    for note in chord_notes:
        if note - 12 >= 36 and rng.random() < 0.3:
            candidates.add(note - 12)
        if note + 12 <= 96 and rng.random() < 0.7:
            candidates.add(note + 12)
        if note + 24 <= 96 and rng.random() < 0.25:
            candidates.add(note + 24)
    notes = sorted(candidates)
    target_count = rng.randint(4, 7) if accent else rng.randint(3, 6)
    if len(notes) > target_count:
        start_index = rng.randint(0, len(notes) - target_count)
        notes = notes[start_index : start_index + target_count]
    if rng.random() < 0.45:
        notes = list(reversed(notes))
    base_time = time.time()
    base_offset = rng.uniform(0.0, 0.8 if accent else 0.5)
    spacing = rng.uniform(0.05, 0.18) * (1.05 - (intensity * 0.35))
    base_release = rng.uniform(14.0, 28.0) if accent else rng.uniform(10.0, 20.0)
    velocity_max = int(52 + (intensity * 52) + (18 if accent else 0))
    velocity_min = 24 if accent else 18
    for i, note in enumerate(notes):
        velocity = rng.randint(velocity_min, max(velocity_min + 1, velocity_max))
        dynamic = velocity_to_dynamic(velocity, max_dynamic)
        sample_index, rate = select_sample(
            float(note), float(dynamic), indices, pitches, max_dynamic
        )
        buffer = buffers[sample_index]
        detune = rng.uniform(0.9975, 1.0025)
        pan = _note_to_pan(note) + rng.uniform(-0.08, 0.08)
        amplitude = supriya.conversions.midi_velocity_to_amplitude(velocity) * (
            0.05 + (intensity * 0.05) + (0.03 if accent else 0.0)
        )
        atk = rng.uniform(0.01, 0.18 if accent else 0.12)
        rel = base_release + rng.uniform(-4.0, 7.0)
        hp = rng.uniform(25.0, 60.0)
        lp = rng.uniform(6000.0, 18000.0)
        offset = base_offset + (i * spacing) + rng.uniform(0.0, 0.035)
        with server.at(base_time + offset):
            server.add_synth(
                ambient_piano_gesture,
                buf=buffer,
                rate=rate * detune,
                pan=pan,
                amp=amplitude,
                atk=atk,
                rel=rel,
                hp=hp,
                lp=lp,
                out=out_bus,
            ) 


def run_background_01(args: argparse.Namespace) -> None:
    intensity = float(args.program_intensity)
    if not (0.0 <= intensity <= 1.0):
        raise ValueError("--intensity must be between 0 and 1")
    rng = random.Random(
        None if args.program_seed is None else int(args.program_seed)
    )
    sample_rate = int(args.program_sample_rate)
    quiet = (
        bool(args.program_quiet)
        if args.program_quiet is not None
        else bool(getattr(args, "quiet", False))
    )

    performance = PERFORMANCE_STYLES["debussy"]
    server = supriya.Server(options=realtime_options(4096, sample_rate=sample_rate)).boot()
    mix_bus = server.add_bus_group(calculation_rate="audio", count=2)
    voice_group = server.add_group(
        add_action="ADD_TO_HEAD", target_node=server.default_group
    )
    fx_group = server.add_group(add_action="ADD_AFTER", target_node=voice_group)
    buffers = load_sample_buffers(server, SAMPLE_PACK)
    indices, pitches, max_dynamic = build_lookup(quiet=quiet)
    server.add_synthdefs(
        piano_synth_room,
        ambient_piano_gesture,
        ambient_piano_grain_cloud,
        ambient_piano_master_fx,
    )
    server.sync()

    server.add_synth(
        ambient_piano_master_fx,
        target_node=fx_group,
        add_action="ADD_TO_HEAD",
        in_bus=mix_bus,
        out=0,
        wet=0.9,
        hp=24.0,
        lp_min=550.0,
        lp_max=14000.0,
        lp_lfo_rate=0.008,
        delay_time=0.48,
        delay_decay=7.0,
        delay_mix=0.18,
        reverb_mix=0.42,
        room_size=0.93,
        damping=0.48,
        shimmer_mix=0.05,
        shimmer_ratio=1.5,
    )

    scale_notes = _build_scale_notes(
        BACKGROUND_01_ROOT,
        BACKGROUND_01_SCALE_OFFSETS,
        low=40,
        high=92,
    )
    if len(scale_notes) < 8:
        raise RuntimeError("Scale configuration produced too few notes.")

    chord_root_index = rng.randint(0, len(scale_notes) - 7)
    chord_notes = _build_scale_chord(scale_notes, chord_root_index)
    fade_time = 8.0
    active_clouds = _spawn_ambient_clouds(
        server,
        buffers=buffers,
        indices=indices,
        pitches=pitches,
        max_dynamic=max_dynamic,
        chord_notes=chord_notes,
        target_node=voice_group,
        out_bus=mix_bus,
        intensity=intensity,
        rng=rng,
        fade_time=fade_time,
    )
    _trigger_ambient_gesture(
        server,
        buffers=buffers,
        indices=indices,
        pitches=pitches,
        max_dynamic=max_dynamic,
        chord_notes=chord_notes,
        out_bus=mix_bus,
        intensity=intensity,
        rng=rng,
        accent=True,
    )

    print("background_01 running. Press Ctrl-C to stop.")
    start = time.monotonic()
    start_wall = time.time()
    last_note = rng.choice(chord_notes)
    energy = intensity
    tempo = 44.0 + (intensity * 18.0) + rng.uniform(-3.0, 3.0)
    tempo_target = tempo

    def to_wall(event_time: float) -> float:
        return start_wall + (event_time - start)

    pattern_steps = rng.choice([8, 12, 16])
    pattern_pulses = max(2, int(pattern_steps * (0.25 + intensity * 0.35)))
    pattern = _euclidean_pattern(pattern_pulses, pattern_steps)
    if pattern:
        shift = rng.randrange(len(pattern))
        pattern = pattern[shift:] + pattern[:shift]
    step_index = 0
    next_step = start + rng.uniform(0.2, 0.6)
    next_phrase = start + rng.uniform(14.0, 22.0)
    next_chord_change = start + rng.uniform(32.0, 55.0)
    next_gesture = start + rng.uniform(10.0, 18.0)
    next_tempo_shift = start + rng.uniform(18.0, 34.0)
    pending_free: list[tuple[float, list[supriya.Synth]]] = []

    try:
        while True:
            now = time.monotonic()
            if args.program_duration is not None and (now - start) >= float(
                args.program_duration
            ):
                break
            if pending_free:
                still_pending: list[tuple[float, list[supriya.Synth]]] = []
                for free_at, synths in pending_free:
                    if now < free_at:
                        still_pending.append((free_at, synths))
                        continue
                    for synth in synths:
                        synth.free()
                pending_free = still_pending
            if now >= next_tempo_shift:
                tempo_target = max(36.0, min(72.0, tempo + rng.uniform(-6.0, 6.0)))
                next_tempo_shift = now + rng.uniform(18.0, 34.0)
            tempo += (tempo_target - tempo) * 0.02
            beat_duration = 60.0 / max(20.0, tempo)
            if now >= next_phrase:
                energy = max(0.0, min(1.0, energy + rng.uniform(-0.18, 0.18)))
                pattern_steps = rng.choice([8, 12, 16])
                pattern_pulses = max(2, int(pattern_steps * (0.25 + energy * 0.4)))
                pattern = _euclidean_pattern(pattern_pulses, pattern_steps)
                if pattern:
                    shift = rng.randrange(len(pattern))
                    pattern = pattern[shift:] + pattern[:shift]
                step_index = 0
                next_phrase = now + rng.uniform(14.0, 24.0)
            if now >= next_chord_change:
                chord_root_index += rng.choice([-2, -1, 0, 1, 2])
                chord_root_index = max(0, min(chord_root_index, len(scale_notes) - 7))
                chord_notes = _build_scale_chord(scale_notes, chord_root_index)
                for synth in active_clouds:
                    synth.set(amp=0.0)
                pending_free.append((now + fade_time + 1.0, active_clouds))
                active_clouds = _spawn_ambient_clouds(
                    server,
                    buffers=buffers,
                    indices=indices,
                    pitches=pitches,
                    max_dynamic=max_dynamic,
                    chord_notes=chord_notes,
                    target_node=voice_group,
                    out_bus=mix_bus,
                    intensity=intensity,
                    rng=rng,
                    fade_time=fade_time,
                )
                _trigger_ambient_gesture(
                    server,
                    buffers=buffers,
                    indices=indices,
                    pitches=pitches,
                    max_dynamic=max_dynamic,
                    chord_notes=chord_notes,
                    out_bus=mix_bus,
                    intensity=intensity,
                    rng=rng,
                    accent=True,
                )
                next_chord_change = now + rng.uniform(30.0, 55.0)
            if now >= next_gesture:
                _trigger_ambient_gesture(
                    server,
                    buffers=buffers,
                    indices=indices,
                    pitches=pitches,
                    max_dynamic=max_dynamic,
                    chord_notes=chord_notes,
                    out_bus=mix_bus,
                    intensity=intensity,
                    rng=rng,
                    accent=False,
                )
                next_gesture = now + rng.uniform(12.0, 22.0)
            if now >= next_step:
                play_step = bool(pattern and pattern[step_index])
                step_index = (step_index + 1) % max(1, len(pattern))
                if play_step and rng.random() < (0.6 + intensity * 0.3):
                    use_chord = rng.random() < (0.65 + energy * 0.2)
                    if use_chord:
                        note = rng.choice(chord_notes)
                    else:
                        scale_index = scale_notes.index(last_note)
                        window = scale_notes[
                            max(0, scale_index - 4) : min(len(scale_notes), scale_index + 5)
                        ]
                        note = rng.choice(window or scale_notes)
                    last_note = note
                    velocity_center = 30 + (energy * 28)
                    velocity_spread = 12 + (energy * 10)
                    velocity = int(
                        max(
                            16,
                            min(
                                84,
                                rng.gauss(velocity_center, velocity_spread),
                            ),
                        )
                    )
                    duration = beat_duration * rng.choice([0.75, 1.0, 1.5, 2.25])
                    _schedule_background_note(
                        server,
                        buffers=buffers,
                        indices=indices,
                        pitches=pitches,
                        max_dynamic=max_dynamic,
                        note=note,
                        velocity=velocity,
                        start_time=to_wall(now + rng.uniform(0.0, 0.12)),
                        duration=duration,
                        performance=performance,
                        out_bus=mix_bus,
                        rng=rng,
                    )
                    if rng.random() < (0.12 + (1.0 - intensity) * 0.18):
                        bass_note = max(32, chord_notes[0] - 12)
                        _schedule_background_note(
                            server,
                            buffers=buffers,
                            indices=indices,
                            pitches=pitches,
                            max_dynamic=max_dynamic,
                            note=bass_note,
                            velocity=max(18, velocity - 8),
                            start_time=to_wall(now + rng.uniform(0.0, 0.2)),
                            duration=beat_duration * rng.uniform(2.0, 3.5),
                            performance=performance,
                            out_bus=mix_bus,
                            rng=rng,
                        )
                step_jitter = rng.uniform(-0.08, 0.1)
                step_multiplier = rng.choice([0.75, 1.0, 1.25])
                step_duration = max(0.12, beat_duration * step_multiplier + step_jitter)
                next_step = now + step_duration
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        server.quit()


def run_ambient_01(args: argparse.Namespace) -> None:
    intensity = float(args.program_intensity)
    if not (0.0 <= intensity <= 1.0):
        raise ValueError("--intensity must be between 0 and 1")
    rng = random.Random(
        None if args.program_seed is None else int(args.program_seed)
    )
    sample_rate = int(args.program_sample_rate)
    quiet = (
        bool(args.program_quiet)
        if args.program_quiet is not None
        else bool(getattr(args, "quiet", False))
    )

    server = supriya.Server(options=realtime_options(2048, sample_rate=sample_rate)).boot()
    mix_bus = server.add_bus_group(calculation_rate="audio", count=2)
    voice_group = server.add_group(
        add_action="ADD_TO_HEAD", target_node=server.default_group
    )
    fx_group = server.add_group(add_action="ADD_AFTER", target_node=voice_group)
    buffers = load_sample_buffers(server, SAMPLE_PACK)
    indices, pitches, max_dynamic = build_lookup(quiet=quiet)
    server.add_synthdefs(
        ambient_piano_gesture,
        ambient_piano_grain_cloud,
        ambient_piano_master_fx,
    )
    server.sync()

    server.add_synth(
        ambient_piano_master_fx,
        target_node=fx_group,
        add_action="ADD_TO_HEAD",
        in_bus=mix_bus,
        out=0,
        wet=0.92,
        hp=28.0,
        lp_min=700.0,
        lp_max=14000.0,
        lp_lfo_rate=0.01,
        delay_time=0.43,
        delay_decay=6.0,
        delay_mix=0.2,
        reverb_mix=0.38,
        room_size=0.92,
        damping=0.45,
        shimmer_mix=0.07,
        shimmer_ratio=1.5,
    )

    chord_index = 0
    fade_time = 8.0
    active_clouds = _spawn_ambient_clouds(
        server,
        buffers=buffers,
        indices=indices,
        pitches=pitches,
        max_dynamic=max_dynamic,
        chord_notes=AMBIENT_01_CHORDS[chord_index],
        target_node=voice_group,
        out_bus=mix_bus,
        intensity=intensity,
        rng=rng,
        fade_time=fade_time,
    )
    _trigger_ambient_gesture(
        server,
        buffers=buffers,
        indices=indices,
        pitches=pitches,
        max_dynamic=max_dynamic,
        chord_notes=AMBIENT_01_CHORDS[chord_index],
        out_bus=mix_bus,
        intensity=intensity,
        rng=rng,
        accent=True,
    )

    print("ambient_01 running. Press Ctrl-C to stop.")
    start = time.monotonic()
    next_gesture = start + rng.uniform(4.0, 8.0)
    gesture_min = max(4.0, 18.0 - (intensity * 12.0))
    gesture_max = max(8.0, 34.0 - (intensity * 20.0))
    next_chord_change = start + rng.uniform(35.0, 55.0)
    chord_min = max(25.0, 70.0 - (intensity * 30.0))
    chord_max = max(40.0, 120.0 - (intensity * 45.0))
    pending_free: list[tuple[float, list[supriya.Synth]]] = []
    try:
        while True:
            now = time.monotonic()
            if args.program_duration is not None and (now - start) >= float(
                args.program_duration
            ):
                break
            if pending_free:
                still_pending: list[tuple[float, list[supriya.Synth]]] = []
                for free_at, synths in pending_free:
                    if now < free_at:
                        still_pending.append((free_at, synths))
                        continue
                    for synth in synths:
                        synth.free()
                pending_free = still_pending
            if now >= next_chord_change:
                chord_index = (chord_index + 1) % len(AMBIENT_01_CHORDS)
                for synth in active_clouds:
                    synth.set(amp=0.0)
                pending_free.append((now + fade_time + 1.0, active_clouds))
                active_clouds = _spawn_ambient_clouds(
                    server,
                    buffers=buffers,
                    indices=indices,
                    pitches=pitches,
                    max_dynamic=max_dynamic,
                    chord_notes=AMBIENT_01_CHORDS[chord_index],
                    target_node=voice_group,
                    out_bus=mix_bus,
                    intensity=intensity,
                    rng=rng,
                    fade_time=fade_time,
                )
                _trigger_ambient_gesture(
                    server,
                    buffers=buffers,
                    indices=indices,
                    pitches=pitches,
                    max_dynamic=max_dynamic,
                    chord_notes=AMBIENT_01_CHORDS[chord_index],
                    out_bus=mix_bus,
                    intensity=intensity,
                    rng=rng,
                    accent=True,
                )
                next_chord_change = now + rng.uniform(chord_min, chord_max)
            if now >= next_gesture:
                _trigger_ambient_gesture(
                    server,
                    buffers=buffers,
                    indices=indices,
                    pitches=pitches,
                    max_dynamic=max_dynamic,
                    chord_notes=AMBIENT_01_CHORDS[chord_index],
                    out_bus=mix_bus,
                    intensity=intensity,
                    rng=rng,
                    accent=False,
                )
                next_gesture = now + rng.uniform(gesture_min, gesture_max)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        server.quit()


PROGRAMS: dict[str, Program] = {
    "background_01": Program(
        name="background_01",
        description="Procedural background piano with evolving harmony and timing",
        runner=run_background_01,
    ),
    "ambient_01": Program(
        name="ambient_01",
        description="Evolving piano ambience with grain clouds and long gestures",
        runner=run_ambient_01,
    ),
    "ambient_02": Program(
        name="ambient_02",
        description="Darker drones and sparse phrases (planned)",
    ),
    "nocturne_01": Program(
        name="nocturne_01",
        description="Slow lyrical fragments and pedal wash (planned)",
    ),
    "minimal_01": Program(
        name="minimal_01",
        description="Repeating figures with subtle variations (planned)",
    ),
}


def list_programs() -> None:
    for program in PROGRAMS.values():
        status = "ready" if program.implemented else "planned"
        print(f"{program.name:12s} [{status}]  {program.description}")


def handle_program(args: argparse.Namespace) -> None:
    if args.program_command == "list":
        list_programs()
        return
    if args.program_command != "run":
        raise RuntimeError(f"Unknown program command {args.program_command}")
    if (program := PROGRAMS.get(args.name)) is None:
        raise RuntimeError(f"Unknown program: {args.name}")
    if not program.implemented or program.runner is None:
        raise RuntimeError(f"Program not implemented yet: {program.name}")
    program.runner(args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render or play an upright piano sampler using the bundled samples"
    )
    subparsers = parser.add_subparsers(dest="command")
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--midi",
        type=Path,
        help="MIDI file to render or play (.mid, .midi, .csv, .midicsv)",
    )
    input_group.add_argument(
        "--midicsv",
        type=Path,
        help="Midicsv file to render or play (.csv or .midicsv)",
    )
    parser.add_argument(
        "--play",
        action="store_true",
        help="Play to system audio instead of rendering a file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("output") / "piano_sampler.wav",
        help="Output WAV file path (default: scripts/output/piano_sampler.wav)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=12.0,
        help="Length of the riff in seconds (default: 12.0)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Use only the two quietest dynamics",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Random seed for stereo panning (default: 0)",
    )
    parser.add_argument(
        "--style",
        choices=sorted(PERFORMANCE_STYLES),
        default="raw",
        help="Playback style preset for MIDI rendering / playback (default: raw)",
    )

    program_parser = subparsers.add_parser(
        "program", help="Generative performance programs (ambient, fragments, etc.)"
    )
    program_subparsers = program_parser.add_subparsers(
        dest="program_command", required=True
    )
    program_subparsers.add_parser("list", help="List available programs")
    program_run_parser = program_subparsers.add_parser("run", help="Run a program")
    program_run_parser.add_argument("name", choices=sorted(PROGRAMS))
    program_run_parser.add_argument(
        "--sample-rate", dest="program_sample_rate", type=int, default=44100
    )
    program_run_parser.add_argument(
        "--duration",
        dest="program_duration",
        type=float,
        default=None,
        help="Stop after N seconds (default: run indefinitely)",
    )
    program_run_parser.add_argument(
        "--intensity",
        dest="program_intensity",
        type=float,
        default=0.6,
        help="0..1 amount of activity (default: 0.6)",
    )
    program_run_parser.add_argument(
        "--seed",
        dest="program_seed",
        type=int,
        default=None,
        help="Random seed for repeatable runs",
    )
    program_run_parser.add_argument(
        "--quiet",
        dest="program_quiet",
        action="store_true",
        default=None,
        help="Use only the two quietest dynamics",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "program":
        handle_program(args)
        raise SystemExit(0)
    midi_path = args.midi or args.midicsv
    performance = PERFORMANCE_STYLES.get(str(args.style), PERFORMANCE_STYLES["raw"])
    if midi_path:
        events = load_note_events(midi_path)
        if args.play:
            play_midi(
                events=events,
                quiet=args.quiet,
                seed=args.seed,
                performance=performance,
            )
            raise SystemExit(0)
        output_path, exit_code = render_midi(
            args.output,
            events=events,
            quiet=args.quiet,
            seed=args.seed,
            performance=performance,
        )
    else:
        if args.play:
            play_riff(duration=args.duration, quiet=args.quiet, seed=args.seed)
            raise SystemExit(0)
        output_path, exit_code = render_riff(
            args.output, duration=args.duration, quiet=args.quiet, seed=args.seed
        )
    if output_path:
        print(f"Rendered to {output_path}")
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
