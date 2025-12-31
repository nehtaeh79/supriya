"""
Percussion sampler built on the VSCO 1 drum pack in ``scripts/samples/21073__sgossner__vsco-1-percussion-library-drums``.

Features
- Multiple curated drum synths (kicks, snares, toms, bongos, sticks) with stereo sample playback and velocity-layered choices.
- Render from MIDI files or MIDICSV.
- Live MIDI input to system audio (python-rtmidi required).
- WAV rendering via non-realtime Score, optional mp3 conversion (ffmpeg) and quick system playback.
- Demo patterns per instrument and an "all drums" demo.
- Generative performance programs (see ``program list`` / ``program run ambient_01``).

MIDI provider notes
- Defaults target General MIDI percussion mappings (channel does not matter; velocity drives sample choice).
- Hi-hat / cymbal MIDI notes are mapped to stick/open hand drums; remap with ``--map 42=ethnic_stick`` style overrides if you prefer other pairings.
- If you supply MIDICSV, include the ``Header`` line so ticks-per-quarter can be read; tempo changes are honored.
- MIDI files require ``mido``. Live MIDI input requires ``python-rtmidi``. Both are optional runtime deps for this script only.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import math
import random
import shutil
import subprocess
import sys
import time
import wave
from pathlib import Path
from typing import Callable, Iterable

if sys.version_info < (3, 10):
    raise SystemExit("Python 3.10+ is required to run drum_sampler.py.")

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

try:
    import supriya
except ImportError as exc:  # pragma: no cover - dependency guard
    raise SystemExit(
        "Install supriya in this environment (e.g., `pip install -e .`) before running drum_sampler.py."
    ) from exc
from supriya import Envelope, synthdef
from supriya.conversions import midi_velocity_to_amplitude
from supriya.enums import DoneAction
from supriya.ugens import (
    AllpassC,
    Balance2,
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

try:  # optional; only needed for MIDI files
    import mido
except ImportError:  # pragma: no cover - optional dependency
    mido = None  # type: ignore

try:  # optional; only needed for live MIDI
    import rtmidi  # type: ignore
    import rtmidi.midiutil  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    rtmidi = None  # type: ignore


SAMPLES_DIR = (
    Path(__file__).with_name("samples")
    / "21073__sgossner__vsco-1-percussion-library-drums"
)
OUTPUT_DIR = Path(__file__).with_name("output") / "drum_sampler"
REALTIME_BUFFER_LOAD_BATCH_SIZE = 24


@dataclasses.dataclass(frozen=True)
class SampleLayer:
    path: Path
    velocity_hint: int
    gain: float = 1.0
    tune_semitones: float = 0.0
    channel_count: int = 2
    buffer: supriya.Buffer | None = None

    @property
    def rate(self) -> float:
        return math.pow(2.0, self.tune_semitones / 12.0)


@dataclasses.dataclass
class Instrument:
    name: str
    description: str
    layers: list[SampleLayer]
    midi_notes: list[int]
    default_pan: float = 0.0
    base_gain: float = 1.0
    _rotation: int = 0

    def choose_layer(self, velocity: int, event_index: int | None = None) -> SampleLayer:
        target = max(1, min(velocity, 127))
        ranked = sorted(
            self.layers, key=lambda layer: abs(layer.velocity_hint - target)
        )
        nearest_distance = abs(ranked[0].velocity_hint - target)
        nearest = [layer for layer in ranked if abs(layer.velocity_hint - target) == nearest_distance]
        if len(nearest) == 1:
            return nearest[0]
        if event_index is not None:
            return nearest[event_index % len(nearest)]
        self._rotation = (self._rotation + 1) % len(nearest)
        return nearest[self._rotation]


@dataclasses.dataclass
class DrumEvent:
    time: float
    instrument: str
    velocity: int
    pan: float | None = None


def read_channel_count(path: Path) -> int:
    with wave.open(str(path), "rb") as handle:
        return handle.getnchannels()


def _layer(filename: str, velocity_hint: int, *, gain: float = 1.0) -> SampleLayer:
    path = SAMPLES_DIR / filename
    return SampleLayer(
        path=path,
        velocity_hint=velocity_hint,
        gain=gain,
        channel_count=read_channel_count(path),
    )


def build_instruments() -> dict[str, Instrument]:
    instruments: dict[str, Instrument] = {}
    instruments["kick_open"] = Instrument(
        name="kick_open",
        description="Open concert bass drum (natural ring)",
        midi_notes=[35, 36],
        default_pan=0.0,
        base_gain=1.0,
        layers=[
            _layer("375280__sgossner__bass-drum-bdrum_ppp_3.wav", 15),
            _layer("375277__sgossner__bass-drum-bdrum_pp_2.wav", 32),
            _layer("375275__sgossner__bass-drum-bdrum_p_1.wav", 48),
            _layer("375262__sgossner__bass-drum-bdrum_mp_1.wav", 64),
            _layer("375257__sgossner__bass-drum-bdrum_f_1.wav", 90),
            _layer("375259__sgossner__bass-drum-bdrum_ff_1.wav", 110),
            _layer("375260__sgossner__bass-drum-bdrum_fff_1.wav", 124),
        ],
    )
    instruments["kick_muted"] = Instrument(
        name="kick_muted",
        description="Damped bass drum for tight hits",
        midi_notes=[34],
        default_pan=0.0,
        base_gain=1.1,
        layers=[
            _layer("375270__sgossner__bass-drum-bdrum_muted_pp_1.wav", 28),
            _layer("375268__sgossner__bass-drum-bdrum_muted_mp_1.wav", 52),
            _layer("375267__sgossner__bass-drum-bdrum_muted_mf_1.wav", 74),
            _layer("375264__sgossner__bass-drum-bdrum_muted_ff_1.wav", 108),
            _layer("375265__sgossner__bass-drum-bdrum_muted_fff_1.wav", 123),
        ],
    )
    instruments["kick_punchy"] = Instrument(
        name="kick_punchy",
        description="Smaller bass drum with brighter top",
        midi_notes=[41],
        default_pan=-0.1,
        base_gain=1.0,
        layers=[
            _layer("375256__sgossner__bass-drum-bdrum3_ppp_1.wav", 20),
            _layer("375255__sgossner__bass-drum-bdrum3_p_1.wav", 45),
            _layer("375254__sgossner__bass-drum-bdrum3_mp_1.wav", 72),
            _layer("375253__sgossner__bass-drum-bdrum3_fff_1.wav", 118),
        ],
    )
    instruments["snare_bright"] = Instrument(
        name="snare_bright",
        description="Tight snare with snares on",
        midi_notes=[38],
        default_pan=-0.05,
        base_gain=0.9,
        layers=[
            _layer("375425__sgossner__snare-snare2_pp_1.wav", 25),
            _layer("375422__sgossner__snare-snare2_p_1.wav", 50),
            _layer("375406__sgossner__snare-snare2_mf_1.wav", 75),
            _layer("375401__sgossner__snare-snare2_f_1.wav", 95),
            _layer("375404__sgossner__snare-snare2_ff_1.wav", 115),
            _layer("375405__sgossner__snare-snare2_fff_1.wav", 124),
        ],
    )
    instruments["snare_warm"] = Instrument(
        name="snare_warm",
        description="Darker snare with longer ring",
        midi_notes=[40],
        default_pan=0.05,
        base_gain=0.92,
        layers=[
            _layer("375390__sgossner__snare-snare1_ppp_1.wav", 20),
            _layer("375389__sgossner__snare-snare1_pp_1.wav", 40),
            _layer("375370__sgossner__snare-snare1_mp_1.wav", 65),
            _layer("375364__sgossner__snare-snare1_f_1.wav", 90),
            _layer("375367__sgossner__snare-snare1_ff_1.wav", 110),
            _layer("375368__sgossner__snare-snare1_fff_1.wav", 124),
        ],
    )
    instruments["snare_rimshot"] = Instrument(
        name="snare_rimshot",
        description="Rimshot accent",
        midi_notes=[39],
        default_pan=-0.08,
        base_gain=0.9,
        layers=[
            _layer("375398__sgossner__snare-snare1_rimshot_mf.wav", 70),
            _layer("375396__sgossner__snare-snare1_rimshot_f.wav", 100),
            _layer("375397__sgossner__snare-snare1_rimshot_fff_1.wav", 120),
        ],
    )
    instruments["side_stick"] = Instrument(
        name="side_stick",
        description="Side-stick / click",
        midi_notes=[37],
        default_pan=-0.12,
        base_gain=0.75,
        layers=[
            _layer("375360__sgossner__snare-snare1_click.wav", 35),
            _layer("375361__sgossner__snare-snare1_click2.wav", 55),
            _layer("375362__sgossner__snare-snare1_click3.wav", 75),
            _layer("375363__sgossner__snare-snare1_click4.wav", 95),
        ],
    )
    instruments["tom_high"] = Instrument(
        name="tom_high",
        description="High tenor tom",
        midi_notes=[48, 50],
        default_pan=-0.2,
        base_gain=0.9,
        layers=[
            _layer("375473__sgossner__tenor-higher-tenorh_pp_1.wav", 30),
            _layer("375468__sgossner__tenor-higher-tenorh_mp_1.wav", 55),
            _layer("375465__sgossner__tenor-higher-tenorh_mf_1.wav", 75),
            _layer("375452__sgossner__tenor-higher-tenorh_f_1.wav", 95),
            _layer("375455__sgossner__tenor-higher-tenorh_ff_1.wav", 115),
        ],
    )
    instruments["tom_low"] = Instrument(
        name="tom_low",
        description="Low tenor / floor tom",
        midi_notes=[45, 47],
        default_pan=0.2,
        base_gain=0.9,
        layers=[
            _layer("375488__sgossner__tenor-lower-tenor_pp_1.wav", 35),
            _layer("375487__sgossner__tenor-lower-tenor_mp_1.wav", 60),
            _layer("375483__sgossner__tenor-lower-tenor_mf_1.wav", 78),
            _layer("375474__sgossner__tenor-lower-tenor_f_1.wav", 96),
            _layer("375476__sgossner__tenor-lower-tenor_ff_1.wav", 116),
        ],
    )
    instruments["bongo_hi"] = Instrument(
        name="bongo_hi",
        description="High bongo (two round-robin layers)",
        midi_notes=[60],
        default_pan=-0.25,
        base_gain=0.8,
        layers=[
            _layer("375288__sgossner__bongos-highbongo1.wav", 60),
            _layer("375289__sgossner__bongos-highbongo2.wav", 95),
        ],
    )
    instruments["bongo_low"] = Instrument(
        name="bongo_low",
        description="Low bongo (two round-robin layers)",
        midi_notes=[61],
        default_pan=0.25,
        base_gain=0.85,
        layers=[
            _layer("375290__sgossner__bongos-lowbongo1.wav", 55),
            _layer("375291__sgossner__bongos-lowbongo2.wav", 90),
        ],
    )
    instruments["ethnic_low_open"] = Instrument(
        name="ethnic_low_open",
        description="Open low drum (works for open hi-hat / cymbal roles)",
        midi_notes=[46, 49, 51],
        default_pan=0.15,
        base_gain=0.95,
        layers=[
            _layer("375308__sgossner__ethnic-ethniclowopen_hit_pp_3.wav", 28),
            _layer("375304__sgossner__ethnic-ethniclowopen_hit_mp_1.wav", 64),
            _layer("375301__sgossner__ethnic-ethniclowopen_hit_f_2.wav", 100),
            _layer("375300__sgossner__ethnic-ethniclowopen_hit_f_1.wav", 118),
        ],
    )
    instruments["ethnic_stick"] = Instrument(
        name="ethnic_stick",
        description="Bright stick-on-drum hit (useful stand-in for closed hats / claves)",
        midi_notes=[42, 44],
        default_pan=-0.3,
        base_gain=0.8,
        layers=[
            _layer("375343__sgossner__ethnic-ethniclargesticks_hit_ppp_1.wav", 20),
            _layer("375341__sgossner__ethnic-ethniclargesticks_hit_p_1.wav", 40),
            _layer("375340__sgossner__ethnic-ethniclargesticks_hit_mp_1.wav", 65),
            _layer("375338__sgossner__ethnic-ethniclargesticks_hit_mf_1.wav", 85),
            _layer("375335__sgossner__ethnic-ethniclargesticks_hit_f_1.wav", 110),
            _layer("375337__sgossner__ethnic-ethniclargesticks_hit_fff_1.wav", 124),
        ],
    )
    instruments["ethnic_hand"] = Instrument(
        name="ethnic_hand",
        description="Soft hand drum / brush texture",
        midi_notes=[68],
        default_pan=0.0,
        base_gain=0.7,
        layers=[
            _layer("375329__sgossner__ethnic-ethniclargehand_hit_ppp_2.wav", 15),
            _layer("375324__sgossner__ethnic-ethniclargehand_hit_pp_1.wav", 35),
            _layer("375323__sgossner__ethnic-ethniclargehand_hit_p_1.wav", 55),
            _layer("375319__sgossner__ethnic-ethniclargehand_hit_mp_1.wav", 75),
            _layer("375314__sgossner__ethnic-ethniclargehand_hit_f_1.wav", 100),
        ],
    )
    return instruments


INSTRUMENTS = build_instruments()


@synthdef()
def drum_voice(
    buffer_id=0,
    rate=1.0,
    amplitude=0.5,
    pan=0.0,
    out=0,
    attack=0.001,
    release=0.5,
    start_position=0.0,
):
    envelope = EnvGen.kr(
        envelope=Envelope.percussive(attack_time=attack, release_time=release),
        done_action=DoneAction.FREE_SYNTH,
    )
    sig = PlayBuf.ar(
        channel_count=2,
        buffer_id=buffer_id,
        rate=BufRateScale.kr(buffer_id=buffer_id) * rate,
        trigger=1,
        start_position=start_position,
        loop=0,
        done_action=DoneAction.NOTHING,
    )
    balanced = Balance2.ar(
        left=sig[0] * envelope,
        right=sig[1] * envelope,
        position=pan,
        level=amplitude,
    )
    Out.ar(bus=out, source=balanced)


@synthdef()
def ambient_grain_cloud(
    buffer_id=0,
    out=0,
    amp=0.12,
    pan=0.0,
    pan_spread=0.35,
    density=3.0,
    base_grain_duration=0.15,
    grain_duration_jitter=0.08,
    base_rate=0.5,
    pitch_mod_semitones=0.0,
    position_mod_rate=0.07,
    filter_min=80.0,
    filter_max=8000.0,
    filter_mod_rate=0.03,
):
    density_lfo = 0.65 + 0.35 * ((LFNoise2.kr(frequency=position_mod_rate * 0.11) + 1) * 0.5)
    trig = Dust.kr(density=density * density_lfo)
    # GrainBuf's position is normalized (0..1). Bias towards the start of the sample
    # to avoid spending too much time in the near-silent tail of percussive recordings.
    position_noise = (LFNoise2.kr(frequency=position_mod_rate) + 1) * 0.5
    position = position_noise**2
    duration_noise = (LFNoise2.kr(frequency=position_mod_rate * 0.617) + 1) * 0.5
    grain_duration = base_grain_duration + (duration_noise * grain_duration_jitter)
    pitch_noise = LFNoise2.kr(frequency=position_mod_rate * 0.431)
    pitch_ratio = 2 ** ((pitch_noise * pitch_mod_semitones) / 12)
    rate = base_rate * pitch_ratio
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
        maximum_overlap=512,
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
    amp_lfo = 0.6 + 0.4 * ((SinOsc.kr(frequency=position_mod_rate * 0.13) + 1) * 0.5)
    Out.ar(bus=out, source=[x * amp * amp_lfo for x in filtered])


@synthdef()
def ambient_master_fx(
    in_bus=0,
    out=0,
    wet=0.85,
    hp=25.0,
    lp_min=900.0,
    lp_max=12000.0,
    lp_lfo_rate=0.011,
    delay_time=0.35,
    delay_decay=5.0,
    delay_mix=0.25,
    reverb_mix=0.35,
    room_size=0.85,
    damping=0.45,
    shimmer_mix=0.08,
    shimmer_ratio=1.5,
):
    source = In.ar(bus=in_bus, channel_count=2)
    lfo = (SinOsc.kr(frequency=lp_lfo_rate) + 1) * 0.5
    cutoff = lp_min + lfo * (lp_max - lp_min)
    shaped = [
        LPF.ar(source=HPF.ar(source=LeakDC.ar(source=source[i]), frequency=hp), frequency=cutoff)
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


@dataclasses.dataclass
class LoadedKit:
    instruments: dict[str, Instrument]
    layers: dict[str, list[SampleLayer]]
    context: supriya.Context

    def trigger(
        self,
        event: DrumEvent,
        *,
        event_index: int | None = None,
        out=0,
        attack: float = 0.001,
        release: float = 0.75,
        rate_scale: float = 1.0,
        start_position: float = 0.0,
    ) -> None:
        instrument = self.instruments[event.instrument]
        template_layer = instrument.choose_layer(event.velocity, event_index)
        loaded_layers = self.layers[event.instrument]
        layer = next(
            (loaded for loaded in loaded_layers if loaded.path == template_layer.path),
            loaded_layers[0],
        )
        if layer.buffer is None:
            raise RuntimeError(f"Buffer not loaded for {event.instrument}")
        amplitude = (
            instrument.base_gain
            * layer.gain
            * midi_velocity_to_amplitude(event.velocity)
        )
        pan = event.pan if event.pan is not None else instrument.default_pan
        moment = (
            self.context.at(event.time)
            if isinstance(self.context, supriya.Score)
            else self.context.at()
        )
        with moment:
            self.context.add_synth(
                drum_voice,
                buffer_id=layer.buffer,
                rate=layer.rate * rate_scale,
                amplitude=amplitude,
                pan=pan,
                out=out,
                attack=attack,
                release=release,
                start_position=start_position,
            )


def load_kit(context: supriya.Context, *, at: float | None = 0.0) -> LoadedKit:
    instruments: dict[str, Instrument] = {}
    layers: dict[str, list[SampleLayer]] = {}
    # For realtime contexts, avoid stuffing hundreds of buffer allocs into a single UDP bundle.
    if isinstance(context, supriya.Score) or at is not None:
        with context.at(at):
            context.add_synthdefs(drum_voice)
            for name, instrument in INSTRUMENTS.items():
                instruments[name] = dataclasses.replace(instrument, _rotation=0)
                loaded_layers: list[SampleLayer] = []
                for layer in instrument.layers:
                    buffer = context.add_buffer(file_path=layer.path)
                    loaded_layers.append(
                        dataclasses.replace(layer, buffer=buffer)
                    )
                layers[name] = loaded_layers
    else:
        with context.at():
            context.add_synthdefs(drum_voice)
        pending: list[tuple[str, SampleLayer]] = []
        batch_size = REALTIME_BUFFER_LOAD_BATCH_SIZE
        for name, instrument in INSTRUMENTS.items():
            instruments[name] = dataclasses.replace(instrument, _rotation=0)
            layers[name] = []
            for layer in instrument.layers:
                pending.append((name, layer))
                if len(pending) >= batch_size:
                    with context.at():
                        for inst_name, inst_layer in pending:
                            buffer = context.add_buffer(file_path=inst_layer.path)
                            layers[inst_name].append(
                                dataclasses.replace(inst_layer, buffer=buffer)
                            )
                    pending.clear()
        if pending:
            with context.at():
                for inst_name, inst_layer in pending:
                    buffer = context.add_buffer(file_path=inst_layer.path)
                    layers[inst_name].append(
                        dataclasses.replace(inst_layer, buffer=buffer)
                    )
    # Realtime buffer reads are asynchronous; ensure buffers have non-zero frame counts
    # before returning so playback and granular UGens don't start on empty buffers.
    if isinstance(context, supriya.BaseServer):
        all_buffers: list[supriya.Buffer] = []
        for instrument_layers in layers.values():
            for layer in instrument_layers:
                if layer.buffer is not None:
                    all_buffers.append(layer.buffer)
        _wait_for_buffers_loaded(context, all_buffers)
    return LoadedKit(instruments=instruments, layers=layers, context=context)


def _wait_for_buffers_loaded(
    server: supriya.BaseServer,
    buffers: Iterable[supriya.Buffer],
    *,
    timeout: float = 30.0,
) -> None:
    deadline = time.monotonic() + timeout
    pending = list(buffers)
    while pending:
        still_pending: list[supriya.Buffer] = []
        for buffer_ in pending:
            info = server.query_buffer(buffer_, sync=True)
            if not info or not info.items:
                still_pending.append(buffer_)
                continue
            item = info.items[0]
            if item.frame_count <= 0:
                still_pending.append(buffer_)
        if not still_pending:
            return
        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"Timed out waiting for {len(still_pending)} buffers to load"
            )
        time.sleep(0.05)
        pending = still_pending


def convert_ticks_to_seconds(
    events: list[tuple[int, int, int]],
    tempos: list[tuple[int, int]],
    ticks_per_beat: int,
) -> list[tuple[float, int, int]]:
    tempo_map = sorted(tempos or [(0, 500_000)], key=lambda t: t[0])
    combined: list[tuple[int, str, int]] = []
    for tick, tempo in tempo_map:
        combined.append((tick, "tempo", tempo))
    for index, (tick, _note, _vel) in enumerate(events):
        combined.append((tick, "event", index))
    combined.sort(key=lambda item: (item[0], 0 if item[1] == "tempo" else 1))
    current_tick = 0
    current_time = 0.0
    current_tempo = tempo_map[0][1]
    event_times = [0.0 for _ in events]
    for tick, kind, value in combined:
        delta_ticks = tick - current_tick
        current_time += delta_ticks * (current_tempo / 1_000_000.0) / ticks_per_beat
        current_tick = tick
        if kind == "tempo":
            current_tempo = value
        else:
            event_times[value] = current_time
    return [
        (event_times[index], note, velocity)
        for index, (_tick, note, velocity) in enumerate(events)
    ]


def parse_midicsv(path: Path) -> tuple[list[tuple[int, int, int]], list[tuple[int, int]], int]:
    ticks_per_beat = 480
    tempos: list[tuple[int, int]] = []
    events: list[tuple[int, int, int]] = []
    with path.open() as handle:
        reader = csv.reader(handle)
        for row in reader:
            if len(row) < 3:
                continue
            time_tick = int(row[1].strip())
            event_type = row[2].strip()
            if event_type == "Header" and len(row) >= 6:
                ticks_per_beat = int(row[5].strip())
            elif event_type == "Tempo" and len(row) >= 4:
                tempos.append((time_tick, int(row[3].strip())))
            elif event_type in {"Note_on_c", "Note_off_c"} and len(row) >= 6:
                note = int(row[4].strip())
                velocity = int(row[5].strip()) if event_type == "Note_on_c" else 0
                if velocity > 0:
                    events.append((time_tick, note, velocity))
    return events, tempos, ticks_per_beat


def parse_midi_file(path: Path) -> tuple[list[tuple[int, int, int]], list[tuple[int, int]], int]:
    if mido is None:
        raise RuntimeError(
            "mido is required for MIDI files. Install with `pip install mido` or provide MIDICSV instead."
        )
    mid = mido.MidiFile(filename=str(path))
    ticks_per_beat = mid.ticks_per_beat
    tempos: list[tuple[int, int]] = []
    events: list[tuple[int, int, int]] = []
    tick_accum = 0
    for msg in mid:
        tick_accum += msg.time
        if msg.type == "set_tempo":
            tempos.append((tick_accum, msg.tempo))
        elif msg.type == "note_on":
            if msg.velocity > 0:
                events.append((tick_accum, msg.note, msg.velocity))
        elif msg.type == "note_off":
            continue
    return events, tempos, ticks_per_beat


def build_events_from_notes(
    timed_events: Iterable[tuple[float, int, int]],
    note_map: dict[int, str],
) -> list[DrumEvent]:
    events: list[DrumEvent] = []
    for time_value, note, velocity in timed_events:
        instrument = note_map.get(note)
        if instrument is None:
            continue
        events.append(
            DrumEvent(
                time=time_value,
                instrument=instrument,
                velocity=velocity,
            )
        )
    if not events:
        return []
    start_time = min(event.time for event in events)
    for event in events:
        event.time -= start_time
    return sorted(events, key=lambda ev: ev.time)


def default_mapping() -> dict[int, str]:
    mapping: dict[int, str] = {}
    for instrument in INSTRUMENTS.values():
        for note in instrument.midi_notes:
            mapping[note] = instrument.name
    mapping.setdefault(49, "ethnic_low_open")
    mapping.setdefault(51, "ethnic_low_open")
    mapping.setdefault(57, "ethnic_low_open")
    return mapping


def apply_mapping_overrides(base: dict[int, str], overrides: list[str]) -> dict[int, str]:
    mapping = dict(base)
    for item in overrides:
        if "=" not in item:
            continue
        note_str, instrument = item.split("=", 1)
        note = int(note_str)
        if instrument not in INSTRUMENTS:
            raise ValueError(f"Unknown instrument {instrument}")
        mapping[note] = instrument
    return mapping


def build_score(
    events: list[DrumEvent],
    *,
    sample_rate: int = 44100,
    tail_seconds: float = 2.5,
) -> supriya.Score:
    score = supriya.Score(output_bus_channel_count=2)
    loaded = load_kit(score, at=0.0)
    for index, event in enumerate(events):
        loaded.trigger(event, event_index=index)
    if events:
        end_time = max(event.time for event in events) + tail_seconds
    else:
        end_time = tail_seconds
    with score.at(end_time):
        score.do_nothing()
    return score


def render_events(
    events: list[DrumEvent],
    *,
    wav_path: Path,
    mp3_path: Path | None,
    sample_rate: int,
) -> Path | None:
    wav_path.parent.mkdir(parents=True, exist_ok=True)
    score = build_score(events, sample_rate=sample_rate)
    output_path, exit_code = supriya.render(
        score,
        output_file_path=wav_path,
        header_format="wav",
        sample_rate=sample_rate,
    )
    if exit_code != 0:
        raise RuntimeError(f"Render failed with exit code {exit_code}")
    if output_path and mp3_path:
        convert_to_mp3(output_path, mp3_path)
    return output_path


def convert_to_mp3(wav_path: Path, mp3_path: Path) -> None:
    if shutil.which("ffmpeg") is None:
        print("ffmpeg not found; skipping mp3 export.")
        return
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", str(wav_path), str(mp3_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result.stderr}")


def play_events_realtime(events: list[DrumEvent], sample_rate: int) -> None:
    server = supriya.Server(options=supriya.Options(sample_rate=sample_rate))
    server.boot()
    loaded = load_kit(server, at=None)
    server.sync()
    start = time.monotonic()
    try:
        for index, event in enumerate(events):
            now = time.monotonic()
            delay = max(0.0, event.time - (now - start))
            if delay:
                time.sleep(delay)
            loaded.trigger(event, event_index=index)
        time.sleep(3.0)
    finally:
        server.quit()


def list_instruments() -> None:
    for instrument in INSTRUMENTS.values():
        notes = ",".join(str(n) for n in instrument.midi_notes)
        print(f"{instrument.name:18s} notes[{notes}]  {instrument.description}")


def demo_events(instrument: str) -> list[DrumEvent]:
    if instrument == "all":
        events: list[DrumEvent] = []
        time_cursor = 0.0
        for name in INSTRUMENTS:
            events.append(DrumEvent(time=time_cursor, instrument=name, velocity=90))
            time_cursor += 0.35
        return events
    if instrument not in INSTRUMENTS:
        raise ValueError(f"Unknown instrument {instrument}")
    velocities = [45, 80, 115]
    return [
        DrumEvent(time=i * 0.4, instrument=instrument, velocity=vel)
        for i, vel in enumerate(velocities)
    ]


@dataclasses.dataclass(frozen=True)
class Program:
    name: str
    description: str
    runner: Callable[[argparse.Namespace], None] | None = None

    @property
    def implemented(self) -> bool:
        return self.runner is not None


def _get_loaded_buffer(kit: LoadedKit, instrument: str, velocity: int, index: int) -> supriya.Buffer:
    instrument_ = kit.instruments[instrument]
    template_layer = instrument_.choose_layer(velocity=velocity, event_index=index)
    loaded_layers = kit.layers[instrument]
    layer = next(
        (loaded for loaded in loaded_layers if loaded.path == template_layer.path),
        loaded_layers[0],
    )
    if layer.buffer is None:
        raise RuntimeError(f"Buffer not loaded for {instrument}")
    return layer.buffer


def _get_layer_path(kit: LoadedKit, instrument: str, velocity: int, index: int) -> Path:
    instrument_ = kit.instruments[instrument]
    layer = instrument_.choose_layer(velocity=velocity, event_index=index)
    return layer.path


def _load_mono_buffers(
    server: supriya.BaseServer,
    paths: Iterable[Path],
) -> dict[Path, supriya.Buffer]:
    # GrainBuf expects mono buffers (SC docs); read only the left channel.
    buffers: dict[Path, supriya.Buffer] = {}
    unique_paths = list(dict.fromkeys(Path(p) for p in paths))
    with server.at():
        for path in unique_paths:
            buffers[path] = server.add_buffer(file_path=path, channel_indices=[0])
    _wait_for_buffers_loaded(server, buffers.values())
    return buffers


def run_ambient_01(args: argparse.Namespace) -> None:
    """
    Evolving ambient background from VSCO percussion samples.

    Starts long-running grain clouds and occasional slow "gesture" hits,
    all routed through a global reverb / delay / shimmer effect.
    """
    intensity = float(args.intensity)
    if not (0.0 <= intensity <= 1.0):
        raise ValueError("--intensity must be between 0 and 1")
    if args.seed is not None:
        random.seed(int(args.seed))
    sample_rate = int(args.sample_rate)

    server = supriya.Server(options=supriya.Options(sample_rate=sample_rate))
    server.boot()
    mix_bus = server.add_bus_group(calculation_rate="audio", count=2)
    mix_bus_base = int(mix_bus)
    voice_group = server.add_group(
        add_action="ADD_TO_HEAD", target_node=server.default_group
    )
    fx_group = server.add_group(add_action="ADD_AFTER", target_node=voice_group)
    kit = load_kit(server, at=None)
    server.add_synthdefs(ambient_grain_cloud, ambient_master_fx)
    server.sync()

    server.add_synth(
        ambient_master_fx,
        target_node=fx_group,
        add_action="ADD_TO_HEAD",
        in_bus=mix_bus_base,
        out=0,
        wet=0.9,
        hp=22.0,
        lp_min=700.0,
        lp_max=14000.0,
        lp_lfo_rate=0.009,
        delay_time=0.42,
        delay_decay=6.0,
        delay_mix=0.18,
        reverb_mix=0.36,
        room_size=0.9,
        damping=0.45,
        shimmer_mix=0.07,
        shimmer_ratio=1.5,
    )

    density_scale = 0.35 + (intensity * 1.25)
    amp_scale = 0.25 + (intensity * 0.75)

    voices = [
        dict(
            instrument="kick_open",
            velocity=110,
            amp=1.32,
            pan=-0.2,
            density=0.8,
            base_grain_duration=0.35,
            grain_duration_jitter=0.18,
            base_rate=0.25,
            pitch_mod_semitones=0.5,
            position_mod_rate=0.03,
            filter_min=35.0,
            filter_max=900.0,
            filter_mod_rate=0.015,
        ),
        dict(
            instrument="kick_muted",
            velocity=80,
            amp=0.88,
            pan=0.2,
            density=0.55,
            base_grain_duration=0.28,
            grain_duration_jitter=0.12,
            base_rate=0.33,
            pitch_mod_semitones=0.25,
            position_mod_rate=0.025,
            filter_min=45.0,
            filter_max=1200.0,
            filter_mod_rate=0.014,
        ),
        dict(
            instrument="snare_warm",
            velocity=95,
            amp=1.10,
            pan=-0.05,
            density=3.5,
            base_grain_duration=0.11,
            grain_duration_jitter=0.07,
            base_rate=0.55,
            pitch_mod_semitones=6.0,
            position_mod_rate=0.07,
            filter_min=160.0,
            filter_max=6500.0,
            filter_mod_rate=0.03,
        ),
        dict(
            instrument="tom_low",
            velocity=90,
            amp=1.10,
            pan=0.1,
            density=2.2,
            base_grain_duration=0.16,
            grain_duration_jitter=0.09,
            base_rate=0.45,
            pitch_mod_semitones=3.0,
            position_mod_rate=0.05,
            filter_min=70.0,
            filter_max=5000.0,
            filter_mod_rate=0.02,
        ),
        dict(
            instrument="ethnic_stick",
            velocity=105,
            amp=0.66,
            pan=-0.35,
            density=5.0,
            base_grain_duration=0.05,
            grain_duration_jitter=0.03,
            base_rate=1.2,
            pitch_mod_semitones=9.0,
            position_mod_rate=0.11,
            filter_min=700.0,
            filter_max=15000.0,
            filter_mod_rate=0.06,
        ),
        dict(
            instrument="ethnic_hand",
            velocity=70,
            amp=0.77,
            pan=0.32,
            density=3.0,
            base_grain_duration=0.09,
            grain_duration_jitter=0.05,
            base_rate=0.75,
            pitch_mod_semitones=4.0,
            position_mod_rate=0.08,
            filter_min=250.0,
            filter_max=9000.0,
            filter_mod_rate=0.04,
        ),
    ]

    grain_paths = [
        _get_layer_path(kit, voice["instrument"], voice["velocity"], i)
        for i, voice in enumerate(voices)
    ]
    mono_buffers = _load_mono_buffers(server, grain_paths)

    for i, voice in enumerate(voices):
        buffer = mono_buffers[_get_layer_path(kit, voice["instrument"], voice["velocity"], i)]
        server.add_synth(
            ambient_grain_cloud,
            target_node=voice_group,
            add_action="ADD_TO_HEAD",
            buffer_id=buffer,
            out=mix_bus_base,
            amp=voice["amp"] * amp_scale,
            pan=voice["pan"],
            density=voice["density"] * density_scale,
            base_grain_duration=voice["base_grain_duration"],
            grain_duration_jitter=voice["grain_duration_jitter"],
            base_rate=voice["base_rate"],
            pitch_mod_semitones=voice["pitch_mod_semitones"],
            position_mod_rate=voice["position_mod_rate"],
            filter_min=voice["filter_min"],
            filter_max=voice["filter_max"],
            filter_mod_rate=voice["filter_mod_rate"],
        )

    # A few immediate gestures so you can hear the program right away.
    kit.trigger(
        DrumEvent(time=0.0, instrument="ethnic_hand", velocity=55, pan=0.2),
        out=mix_bus_base,
        attack=0.02,
        release=12.0,
        rate_scale=0.9,
    )
    kit.trigger(
        DrumEvent(time=0.0, instrument="tom_low", velocity=48, pan=-0.15),
        out=mix_bus_base,
        attack=0.02,
        release=10.0,
        rate_scale=0.6,
    )

    gesture_instruments = [
        "snare_warm",
        "snare_rimshot",
        "tom_high",
        "tom_low",
        "bongo_hi",
        "bongo_low",
        "ethnic_low_open",
        "kick_punchy",
    ]

    print("ambient_01 running. Press Ctrl-C to stop.")
    start = time.monotonic()
    next_gesture = start + random.uniform(4.0, 8.0)
    gesture_min = max(4.0, 14.0 - (intensity * 10.0))
    gesture_max = max(8.0, 28.0 - (intensity * 16.0))
    try:
        while True:
            now = time.monotonic()
            if args.duration is not None and (now - start) >= float(args.duration):
                break
            if now >= next_gesture:
                instrument = random.choice(gesture_instruments)
                velocity = random.randint(28, 70)
                pan = random.uniform(-0.5, 0.5)
                release = random.uniform(5.0, 14.0)
                rate_scale = random.choice([0.25, 0.5, 0.75, 1.0, 1.5]) * random.uniform(
                    0.9, 1.1
                )
                kit.trigger(
                    DrumEvent(time=0.0, instrument=instrument, velocity=velocity, pan=pan),
                    out=mix_bus_base,
                    attack=0.02,
                    release=release,
                    rate_scale=rate_scale,
                )
                next_gesture = now + random.uniform(gesture_min, gesture_max)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        server.quit()


PROGRAMS: dict[str, Program] = {
    "ambient_01": Program(
        name="ambient_01",
        description="Evolving ambient background from VSCO percussion samples",
        runner=run_ambient_01,
    ),
    "ambient_02": Program(
        name="ambient_02",
        description="Darker drones and long swells (planned)",
    ),
    "groove_01": Program(
        name="groove_01",
        description="Straight-ahead kit groove with fills (planned)",
    ),
    "cinematic_01": Program(
        name="cinematic_01",
        description="Sparse cinematic percussion bed (planned)",
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
    parser = argparse.ArgumentParser(description="VSCO percussion sampler for scsynth")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List available instruments and default MIDI notes")

    demo_parser = subparsers.add_parser("demo", help="Render or play a demo pattern")
    demo_parser.add_argument(
        "--instrument",
        default="all",
        help="Instrument name or 'all' (default)",
    )
    demo_parser.add_argument(
        "--play",
        action="store_true",
        help="Play through system audio in realtime instead of rendering",
    )
    demo_parser.add_argument(
        "--wav",
        type=Path,
        help="Optional WAV output path",
    )
    demo_parser.add_argument(
        "--mp3",
        type=Path,
        help="Optional mp3 output path (requires ffmpeg)",
    )
    demo_parser.add_argument("--sample-rate", type=int, default=44100)

    midi_parser = subparsers.add_parser("render-midi", help="Render from a MIDI file")
    midi_parser.add_argument("midi_path", type=Path)
    midi_parser.add_argument("--wav", type=Path, help="WAV output path")
    midi_parser.add_argument("--mp3", type=Path, help="mp3 output path")
    midi_parser.add_argument("--sample-rate", type=int, default=44100)
    midi_parser.add_argument(
        "--map",
        action="append",
        default=[],
        help="Override note mapping like 42=ethnic_stick (repeatable)",
    )

    midicsv_parser = subparsers.add_parser(
        "render-midicsv", help="Render from a MIDICSV file"
    )
    midicsv_parser.add_argument("csv_path", type=Path)
    midicsv_parser.add_argument("--wav", type=Path, help="WAV output path")
    midicsv_parser.add_argument("--mp3", type=Path, help="mp3 output path")
    midicsv_parser.add_argument("--sample-rate", type=int, default=44100)
    midicsv_parser.add_argument(
        "--map",
        action="append",
        default=[],
        help="Override note mapping like 42=ethnic_stick (repeatable)",
    )

    midi_in_parser = subparsers.add_parser("midi-in", help="Play live from a MIDI port")
    midi_in_parser.add_argument(
        "--list-ports",
        action="store_true",
        help="List MIDI input ports and exit",
    )
    midi_in_parser.add_argument(
        "--port",
        type=int,
        help="MIDI input port number",
    )
    midi_in_parser.add_argument(
        "--map",
        action="append",
        default=[],
        help="Override note mapping like 42=ethnic_stick (repeatable)",
    )
    midi_in_parser.add_argument("--sample-rate", type=int, default=44100)

    program_parser = subparsers.add_parser(
        "program", help="Generative performance programs (ambient, grooves, etc.)"
    )
    program_subparsers = program_parser.add_subparsers(
        dest="program_command", required=True
    )
    program_subparsers.add_parser("list", help="List available programs")
    program_run_parser = program_subparsers.add_parser("run", help="Run a program")
    program_run_parser.add_argument("name", choices=sorted(PROGRAMS))
    program_run_parser.add_argument("--sample-rate", type=int, default=44100)
    program_run_parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Stop after N seconds (default: run indefinitely)",
    )
    program_run_parser.add_argument(
        "--intensity",
        type=float,
        default=0.6,
        help="0..1 amount of activity (default: 0.6)",
    )
    program_run_parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for repeatable runs",
    )

    return parser.parse_args()


def handle_demo(args: argparse.Namespace) -> None:
    events = demo_events(args.instrument)
    if args.play:
        play_events_realtime(events, sample_rate=args.sample_rate)
        return
    wav_path = args.wav or OUTPUT_DIR / f"demo_{args.instrument}.wav"
    render_events(
        events,
        wav_path=wav_path,
        mp3_path=args.mp3,
        sample_rate=args.sample_rate,
    )
    print(f"Rendered {wav_path}")
    if args.mp3:
        print(f"Wrote {args.mp3}")


def handle_midi_render(args: argparse.Namespace, *, use_csv: bool) -> None:
    mapping = apply_mapping_overrides(default_mapping(), args.map)
    if use_csv:
        raw_events, tempos, tpq = parse_midicsv(args.csv_path)
    else:
        raw_events, tempos, tpq = parse_midi_file(args.midi_path)
    timed = convert_ticks_to_seconds(raw_events, tempos, tpq)
    events = build_events_from_notes(timed, mapping)
    if not events:
        raise RuntimeError("No mapped note-on events found.")
    source_name = args.csv_path.stem if use_csv else args.midi_path.stem
    wav_path = args.wav or OUTPUT_DIR / f"{source_name}.wav"
    render_events(
        events,
        wav_path=wav_path,
        mp3_path=args.mp3,
        sample_rate=args.sample_rate,
    )
    print(f"Rendered {wav_path}")
    if args.mp3:
        print(f"Wrote {args.mp3}")


def handle_midi_in(args: argparse.Namespace) -> None:
    if rtmidi is None:
        raise RuntimeError(
            "python-rtmidi is required for live MIDI. Install with `pip install python-rtmidi`."
        )
    if args.list_ports:
        rtmidi.midiutil.list_input_ports()
        return
    if args.port is None:
        raise RuntimeError("Provide --port or --list-ports.")
    mapping = apply_mapping_overrides(default_mapping(), args.map)
    midi_in = rtmidi.MidiIn()
    midi_in.open_port(args.port)
    server = supriya.Server(options=supriya.Options(sample_rate=args.sample_rate))
    server.boot()
    loaded = load_kit(server, at=None)
    server.sync()
    print("Listening for MIDI. Ctrl-C to exit.")

    def callback(event, _data=None):
        message, _delta = event
        status = message[0] & 0xF0
        note = message[1]
        velocity = message[2]
        if status == 0x90 and velocity > 0:
            instrument = mapping.get(note)
            if instrument is None:
                return
            loaded.trigger(
                DrumEvent(time=0.0, instrument=instrument, velocity=velocity)
            )

    midi_in.set_callback(callback)
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        midi_in.close_port()
        server.quit()


def main() -> None:
    args = parse_args()
    if args.command == "list":
        list_instruments()
    elif args.command == "demo":
        handle_demo(args)
    elif args.command == "render-midi":
        handle_midi_render(args, use_csv=False)
    elif args.command == "render-midicsv":
        handle_midi_render(args, use_csv=True)
    elif args.command == "midi-in":
        handle_midi_in(args)
    elif args.command == "program":
        handle_program(args)
    else:
        raise RuntimeError(f"Unknown command {args.command}")


if __name__ == "__main__":
    main()
