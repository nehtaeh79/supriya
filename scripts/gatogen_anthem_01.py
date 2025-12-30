"""
Render a non-realtime "Gatogen Anthem" cue inspired by the original
SuperCollider patch.

Note: SuperCollider's scsynth must be installed and available on your PATH
for non-realtime rendering to work.
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

import supriya
from supriya import Envelope, synthdef
from supriya.enums import AddAction, CalculationRate
from supriya.scsynth import Options
from supriya.ugens import (
    AllpassN,
    BPF,
    CombC,
    Compander,
    Demand,
    Dxrand,
    EnvGen,
    FreeVerb2,
    HPF,
    Impulse,
    In,
    LFSaw,
    LFNoise0,
    LFNoise1,
    LFNoise2,
    Latch,
    LeakDC,
    Limiter,
    LocalIn,
    LocalOut,
    Mix,
    Out,
    Pan2,
    PinkNoise,
    Pluck,
    Pulse,
    RLPF,
    Rand,
    Saw,
    SinOsc,
    Splay,
    VarSaw,
    WhiteNoise,
)


def midi_to_hz(note: float) -> float:
    return 440.0 * (2.0 ** ((note - 69.0) / 12.0))


@synthdef()
def master_out(in_=0, out=0, gain=0.85):
    sig = In.ar(bus=in_, channel_count=2)
    sig = LeakDC.ar(sig)
    sig = HPF.ar(sig, 25)
    sig = Compander.ar(
        sig,
        sig,
        thresh=0.22,
        slope_below=1.0,
        slope_above=0.32,
        clamp_time=0.01,
        relax_time=0.12,
    )
    sig = (sig * gain).tanh()
    sig = Limiter.ar(sig, 0.95, 0.01)
    Out.ar(bus=out, source=sig)


@synthdef()
def reverb(in_=0, out=0, mix=0.18, room=0.86, damp=0.45):
    sig = In.ar(bus=in_, channel_count=2)
    sig = FreeVerb2.ar(sig[0], sig[1], mix, room, damp)
    Out.ar(bus=out, source=sig)


@synthdef()
def delay(in_=0, out=0, time=0.33, decay=3.2, mix=0.22):
    sig = In.ar(bus=in_, channel_count=2)
    del_sig = CombC.ar(sig, 1.0, time.clip(0.02, 0.95), decay.clip(0.2, 12.0))
    Out.ar(bus=out, source=sig + (del_sig * mix))


@synthdef()
def kick(out=0, send_rev=0, send_del=0, amp=0.9):
    env = EnvGen.kr(Envelope.percussive(0.001, 0.28, curve=-6), done_action=2)
    fenv = EnvGen.kr(Envelope([82, 34, 28], [0.02, 0.18], curve=-8))
    sig = SinOsc.ar(fenv) * env
    click = BPF.ar(WhiteNoise.ar(0.35), 2200, 0.15) * EnvGen.kr(
        Envelope.percussive(0.001, 0.03), done_action=0
    )
    sig = (sig + click).tanh()
    sig = [sig, sig]
    Out.ar(bus=out, source=sig * amp)
    Out.ar(bus=send_rev, source=sig * amp * 0.03)
    Out.ar(bus=send_del, source=sig * amp * 0.02)


@synthdef()
def snare(out=0, send_rev=0, send_del=0, amp=0.35):
    env = EnvGen.kr(Envelope.percussive(0.002, 0.22, curve=-4), done_action=2)
    nenv = EnvGen.kr(Envelope.percussive(0.001, 0.16, curve=-2), done_action=0)
    body = SinOsc.ar(190, 0, 0.35) + SinOsc.ar(330, 0, 0.18)
    noise = BPF.ar(WhiteNoise.ar(1), 2800, 0.35) * nenv
    sig = (body * env) + noise
    sig = HPF.ar(sig, 120)
    sig = sig.tanh()
    sig = [sig, sig]
    Out.ar(bus=out, source=sig * amp)
    Out.ar(bus=send_rev, source=sig * amp * 0.22)
    Out.ar(bus=send_del, source=sig * amp * 0.06)


@synthdef()
def hat(out=0, send_rev=0, send_del=0, amp=0.14, bright=0.6):
    env = EnvGen.kr(Envelope.percussive(0.001, 0.06, curve=-6), done_action=2)
    sig = WhiteNoise.ar(1) * env
    hp = bright.linexp(0, 1, 6000, 12000)
    sig = HPF.ar(sig, hp)
    sig = BPF.ar(sig, hp * 1.1, 0.6)
    sig = sig.tanh()
    sig = [sig, sig]
    Out.ar(bus=out, source=sig * amp)
    Out.ar(bus=send_rev, source=sig * amp * 0.06)
    Out.ar(bus=send_del, source=sig * amp * 0.12)


@synthdef()
def bass(out=0, send_rev=0, send_del=0, amp=0.22, freq=55, sustain=0.12, bright=0.2, drive=1.4):
    env = EnvGen.kr(
        Envelope.percussive(0.002, sustain.max(0.03), curve=-5), done_action=2
    )
    fenv = EnvGen.kr(Envelope([0.0, 1.0, 0.0], [0.01, sustain.max(0.03)], curve=-6))
    osc = VarSaw.ar(freq * [1, 1.005], 0, 0.45).sum() * 0.5
    sub = SinOsc.ar(freq * 0.5, 0, 0.45)
    cut = bright.linexp(0, 1, 180, 5200) * (1 + (fenv * 2.2))
    sig = (osc + sub) * env
    sig = RLPF.ar(sig, cut, 0.12 + (bright * 0.25))
    sig = (sig * drive).tanh()
    sig = Pan2.ar(sig, LFNoise1.kr(0.25).range(-0.05, 0.05))
    Out.ar(bus=out, source=sig * amp)
    Out.ar(bus=send_rev, source=sig * amp * 0.05)
    Out.ar(bus=send_del, source=sig * amp * 0.03)


@synthdef()
def pad(out=0, send_rev=0, send_del=0, amp=0.10, freq=220, sustain=6, bright=0.15, motion=0.35):
    env = EnvGen.kr(
        Envelope.linen(0.6, sustain.max(0.5), 1.2, curve=-3), done_action=2
    )
    det = [0.0, 0.008, -0.011, 0.015]
    wob = SinOsc.kr(0.08 + (motion * 0.18)).range(0.98, 1.02)
    osc = Mix.new(VarSaw.ar(freq * wob * (1 + det), 0, 0.35)) * 0.35
    noise = PinkNoise.ar(0.06) * (0.4 + (motion * 0.6))
    sig = (osc + noise) * env
    cut = bright.linexp(0, 1, 350, 6500) * (
        1 + SinOsc.kr(0.03 + (motion * 0.07)).range(-0.25, 0.35)
    )
    sig = RLPF.ar(sig, cut, 0.15 + (motion * 0.35))
    sig = AllpassN.ar(sig, 0.2, [Rand.ir(0.02, 0.12), Rand.ir(0.02, 0.12)], 2)
    sig = Splay.ar([sig, sig], 0.5, 1).sum()
    sig = LeakDC.ar(sig).tanh()
    Out.ar(bus=out, source=sig * amp)
    Out.ar(bus=send_rev, source=sig * amp * 0.45)
    Out.ar(bus=send_del, source=sig * amp * 0.10)


@synthdef()
def pluck(out=0, send_rev=0, send_del=0, amp=0.12, freq=440, sustain=0.25, bright=0.5):
    trig = Impulse.ar(0)
    src = PinkNoise.ar(0.55)
    sig = Pluck.ar(src, trig, 0.2, (1 / freq).clip(0.002, 0.2), sustain.max(0.05) * 2.0, 0.35)
    env = EnvGen.kr(
        Envelope.percussive(0.002, sustain.max(0.05), curve=-5), done_action=2
    )
    cut = bright.linexp(0, 1, 800, 9000)
    sig = RLPF.ar(sig, cut, 0.25)
    sig = Pan2.ar(sig, LFNoise1.kr(0.9).range(-0.7, 0.7))
    sig = sig.tanh()
    Out.ar(bus=out, source=sig * amp * env)
    Out.ar(bus=send_rev, source=sig * amp * 0.30 * env)
    Out.ar(bus=send_del, source=sig * amp * 0.35 * env)


@synthdef()
def lead(out=0, send_rev=0, send_del=0, amp=0.11, freq=440, sustain=0.35, bright=0.8, bite=0.4):
    env = EnvGen.kr(
        Envelope.percussive(0.005, sustain.max(0.06), curve=-4), done_action=2
    )
    vib = SinOsc.kr(5.2 + (bite * 4)).range(0.995, 1.005)
    osc = Mix.new(Saw.ar(freq * vib * [1, 1.01, 0.5])) * 0.25
    cut = bright.linexp(0, 1, 1200, 11000) * (1 + (env * 0.6))
    sig = RLPF.ar(osc, cut, 0.12 + (bite * 0.25))
    sig = sig + (BPF.ar(WhiteNoise.ar(0.04 + (bite * 0.06)), cut * 0.8, 0.3) * env)
    sig = (sig * (1.4 + bite)).tanh()
    sig = Pan2.ar(sig, SinOsc.kr(0.12).range(-0.4, 0.4))
    Out.ar(bus=out, source=sig * amp)
    Out.ar(bus=send_rev, source=sig * amp * 0.35)
    Out.ar(bus=send_del, source=sig * amp * 0.40)


@synthdef()
def glitch_hit(out=0, send_rev=0, send_del=0, amp=0.10, freq=900, dur=0.07, crush=0.55, pan=0):
    env = EnvGen.kr(Envelope.percussive(0.001, dur.max(0.02), curve=-7), done_action=2)
    sig = (SinOsc.ar(freq * [1, 1.007]).sum() * 0.5) + (LFSaw.ar(freq * 0.5, 0, 0.25))
    sig = sig + (WhiteNoise.ar(0.28) * env)
    sig = BPF.ar(sig, freq * 2.2, 0.18)
    sig = sig * (1 + (LFNoise0.kr(60).range(-0.25, 0.25)))
    sig = sig.tanh()
    rate = (1 - crush).linexp(0, 1, 250, 9000)
    sig = Latch.ar(sig, Impulse.ar(rate))
    sig = (sig * (2**8)).round() / (2**8)
    sig = Pan2.ar(sig, pan)
    Out.ar(bus=out, source=sig * amp)
    Out.ar(bus=send_rev, source=sig * amp * 0.15)
    Out.ar(bus=send_del, source=sig * amp * 0.55)


@synthdef()
def modem(out=0, send_rev=0, send_del=0, amp=0.10, dur=0.5, pan=0):
    env = EnvGen.kr(Envelope.percussive(0.001, dur.max(0.05), curve=-3), done_action=2)
    rate = LFNoise0.kr(14).range(5, 16)
    freq = Demand.kr(Impulse.kr(rate), 0, Dxrand([260, 390, 520, 780, 1040, 1320, 1560, 2080], math.inf))
    sig = SinOsc.ar(freq) * env
    sig = sig + (BPF.ar(WhiteNoise.ar(0.18), freq * 2, 0.18) * env)
    sig = (sig * 2.0).tanh()
    sig = Pan2.ar(sig, pan)
    Out.ar(bus=out, source=sig * amp)
    Out.ar(bus=send_rev, source=sig * amp * 0.30)
    Out.ar(bus=send_del, source=sig * amp * 0.45)


@synthdef()
def riser(out=0, send_rev=0, send_del=0, amp=0.16, dur=4.0):
    env = EnvGen.kr(Envelope.linen(0.05, dur.max(0.2), 0.2, curve=-2), done_action=2)
    fenv = EnvGen.kr(Envelope([300, 12000], [dur.max(0.2)], curve=3))
    sig = WhiteNoise.ar(1)
    sig = BPF.ar(sig, fenv, 0.25)
    sig = sig + (SinOsc.ar(fenv * 0.25, 0, 0.25))
    sig = (sig * 1.8).tanh()
    sig = Pan2.ar(sig, SinOsc.kr(0.3).range(-0.6, 0.6))
    Out.ar(bus=out, source=sig * amp * env)
    Out.ar(bus=send_rev, source=sig * amp * 0.55 * env)
    Out.ar(bus=send_del, source=sig * amp * 0.30 * env)


@synthdef()
def crash(out=0, send_rev=0, send_del=0, amp=0.55):
    env = EnvGen.kr(Envelope.percussive(0.001, 1.4, curve=-2), done_action=2)
    fenv = EnvGen.kr(Envelope([12000, 250, 80], [0.06, 1.2], curve=-6))
    sig = WhiteNoise.ar(1) + PinkNoise.ar(0.7)
    sig = BPF.ar(sig, fenv, 0.18)
    sig = sig + (SinOsc.ar(fenv * 0.25, 0, 0.3))
    sig = HPF.ar(sig, 35)
    sig = (sig * 4.0).tanh()
    sig = [sig, sig]
    Out.ar(bus=out, source=sig * amp * env)
    Out.ar(bus=send_rev, source=sig * amp * 0.65 * env)
    Out.ar(bus=send_del, source=sig * amp * 0.20 * env)


@synthdef()
def swarm(out=0, send_rev=0, send_del=0, amp=0.08, base=110, life=10, chaos=0.6):
    env = EnvGen.kr(Envelope.linen(0.5, life.max(0.5), 2.0, curve=-3), done_action=2)
    spread = chaos.linlin(0, 1, 0.2, 0.95)
    voices = []
    for i in range(12):
        det = ((i - 6) / 12) * 0.015
        freq = base * (1 + det + LFNoise1.kr(0.04 + (chaos * 0.15)).range(-0.008, 0.008))
        fm = SinOsc.ar(freq * (1.0 + (i * 0.03)), 0, freq * chaos * 0.02)
        osc = Pulse.ar(freq + fm, LFNoise2.kr(0.25).range(0.08, 0.92), 0.35)
        ring = osc * SinOsc.ar((freq * 2) + (fm * 1.5), 0, 0.5)
        noise = BPF.ar(WhiteNoise.ar(0.02 * chaos), freq * 4, 0.25)
        voices.append(
            RLPF.ar(
                ring + noise,
                (freq * (3.5 + LFNoise1.kr(0.1).range(-1, 1) * chaos)).clip(160, 9000),
                0.06 + (chaos * 0.55),
            )
        )
    sig = Splay.ar(voices, spread, 1).sum()
    sig = LeakDC.ar(sig)
    sig = (sig * (1.6 + chaos)).tanh()
    sig = sig * env
    Out.ar(bus=out, source=sig * amp)
    Out.ar(bus=send_rev, source=sig * amp * 0.55)
    Out.ar(bus=send_del, source=sig * amp * 0.25)


@synthdef()
def patchlet(out=0, send_rev=0, send_del=0, amp=0.03, freq=110, life=6, chaos=0.5, pan=0):
    env = EnvGen.kr(Envelope.linen(0.01, life.max(0.2), 0.8, curve=-3), done_action=2)
    mod_a = LFNoise1.kr(0.15 + (chaos * 1.8)).range(0.15, 9.0)
    mod_b = LFNoise2.kr(0.10 + (chaos * 0.9)).range(0.0, 1.0)
    sig = SinOsc.ar(freq * (1 + (SinOsc.ar(freq * mod_a) * mod_b * chaos * 0.35)), 0, 0.5)
    sig = sig + VarSaw.ar(freq * (1 + (LFNoise0.kr(8 + (chaos * 20)) * 0.01)), 0, 0.3)
    sig = sig * env
    fb = LocalIn.ar(2)
    sig = sig + (fb.sum() * 0.12 * chaos)
    sig = RLPF.ar(
        sig,
        (freq * 8).clip(200, 9000) * (1 + (LFNoise1.kr(0.12).range(-0.6, 0.6) * chaos)),
        0.10 + (chaos * 0.65),
    )
    sig = AllpassN.ar(sig, 0.08, [Rand.ir(0.002, 0.06), Rand.ir(0.002, 0.06)], 1.6)
    sig = LeakDC.ar(sig)
    sig = (sig * (1.6 + chaos)).tanh()
    LocalOut.ar([sig, sig])
    sig = Pan2.ar(sig, pan)
    Out.ar(bus=out, source=sig * amp)
    Out.ar(bus=send_rev, source=sig * amp * (0.35 + (chaos * 0.35)))
    Out.ar(bus=send_del, source=sig * amp * (0.18 + (chaos * 0.25)))


def schedule_pattern(score, start, end, step, callback):
    time = start
    while time < end:
        callback(time)
        time += step


def spawn_patch_cloud(score, group, mix_bus, rev_bus, del_bus, rng, time, count=64, base=110, chaos=0.6, life=7, amp=0.02):
    for _ in range(count):
        freq = base * (2 ** rng.uniform(-1.0, 2.0))
        score.add_synth(
            patchlet,
            add_action=AddAction.ADD_TO_HEAD,
            target_node=group,
            out=mix_bus,
            send_rev=rev_bus,
            send_del=del_bus,
            freq=freq,
            chaos=max(0.05, min(1.0, chaos * rng.uniform(0.6, 1.4))),
            life=max(0.3, min(18.0, life * rng.uniform(0.6, 1.4))),
            amp=max(0.0005, min(0.06, amp * rng.uniform(0.35, 1.2))),
            pan=rng.uniform(-1.0, 1.0),
        )


def build_score(output_path: Path) -> tuple[Path | None, int]:
    options = Options(
        memory_size=32768,
        buffer_count=2048,
        maximum_node_count=32768,
        maximum_synthdef_count=2048,
    )
    tempo = 132 / 60.0
    beat = 1.0 / tempo
    rng = random.Random(20240210)

    score = supriya.Score(options=options, output_bus_channel_count=2)
    with score.at(0):
        score.add_synthdefs(
            master_out,
            reverb,
            delay,
            kick,
            snare,
            hat,
            bass,
            pad,
            pluck,
            lead,
            glitch_hit,
            modem,
            riser,
            crash,
            swarm,
            patchlet,
        )
        mix_bus = score.add_bus_group(CalculationRate.AUDIO, 2)
        rev_bus = score.add_bus_group(CalculationRate.AUDIO, 2)
        del_bus = score.add_bus_group(CalculationRate.AUDIO, 2)
        g_main = score.add_group()
        g_patch = score.add_group(add_action=AddAction.ADD_AFTER, target_node=g_main)
        g_fx = score.add_group(add_action=AddAction.ADD_AFTER, target_node=g_patch)
        g_master = score.add_group(add_action=AddAction.ADD_AFTER, target_node=g_fx)
        score.add_synth(
            reverb,
            add_action=AddAction.ADD_TO_TAIL,
            target_node=g_fx,
            in_=int(rev_bus),
            out=int(mix_bus),
            mix=0.14,
            room=0.86,
            damp=0.42,
        )
        score.add_synth(
            delay,
            add_action=AddAction.ADD_TO_TAIL,
            target_node=g_fx,
            in_=int(del_bus),
            out=int(mix_bus),
            time=0.33,
            decay=3.8,
            mix=0.18,
        )
        score.add_synth(
            master_out,
            add_action=AddAction.ADD_TO_TAIL,
            target_node=g_master,
            in_=int(mix_bus),
            out=0,
            gain=0.88,
        )

    prog_roots = [57, 53, 60, 55]
    arp_steps = [0, 7, 12, 7, 0, 3, 7, 10]

    def prog_root_at(beat_index: int) -> float:
        return prog_roots[(beat_index // 8) % len(prog_roots)]

    def schedule_pad(start, end):
        def add_pad(time):
            beat_index = int(time / beat)
            freq = midi_to_hz(prog_root_at(beat_index))
            score.add_synth(
                pad,
                add_action=AddAction.ADD_TO_HEAD,
                target_node=g_main,
                out=int(mix_bus),
                send_rev=int(rev_bus),
                send_del=int(del_bus),
                freq=freq,
                sustain=7.5,
                amp=0.06,
                bright=0.10,
                motion=0.35,
            )

        schedule_pattern(score, start, end, beat * 8, add_pad)

    def schedule_bass(start, end, amp=0.10, bright=0.10, drive=1.2):
        def add_bass(time):
            beat_index = int(time / beat)
            step = arp_steps[beat_index % len(arp_steps)]
            freq = midi_to_hz(prog_root_at(beat_index) + step)
            score.add_synth(
                bass,
                add_action=AddAction.ADD_TO_HEAD,
                target_node=g_main,
                out=int(mix_bus),
                send_rev=int(rev_bus),
                send_del=int(del_bus),
                freq=freq,
                sustain=0.10,
                amp=amp,
                bright=bright,
                drive=drive,
            )

        schedule_pattern(score, start, end, beat / 4, add_bass)

    def schedule_kick(start, end, amp=0.62):
        def add_kick(time):
            score.add_synth(
                kick,
                add_action=AddAction.ADD_TO_HEAD,
                target_node=g_main,
                out=int(mix_bus),
                send_rev=int(rev_bus),
                send_del=int(del_bus),
                amp=amp,
            )

        schedule_pattern(score, start, end, beat, add_kick)

    def schedule_snare(start, end, amp=0.36):
        def add_snare(time):
            if int(time / beat) % 2 == 1:
                score.add_synth(
                    snare,
                    add_action=AddAction.ADD_TO_HEAD,
                    target_node=g_main,
                    out=int(mix_bus),
                    send_rev=int(rev_bus),
                    send_del=int(del_bus),
                    amp=amp,
                )

        schedule_pattern(score, start, end, beat, add_snare)

    def schedule_hat(start, end, amp=0.12):
        def add_hat(time):
            choice = rng.random()
            hat_amp = 0.0
            if choice > 0.75:
                hat_amp = amp
            elif choice > 0.25:
                hat_amp = amp * 0.8
            if hat_amp > 0:
                score.add_synth(
                    hat,
                    add_action=AddAction.ADD_TO_HEAD,
                    target_node=g_main,
                    out=int(mix_bus),
                    send_rev=int(rev_bus),
                    send_del=int(del_bus),
                    amp=hat_amp,
                    bright=0.55,
                )

        schedule_pattern(score, start, end, beat / 4, add_hat)

    def schedule_pluck(start, end, amp=0.08):
        def add_pluck(time):
            beat_index = int(time / beat)
            root = prog_root_at(beat_index)
            intervals = [0, 3, 7, 10, 12, 14]
            freq = midi_to_hz(root + rng.choice(intervals))
            score.add_synth(
                pluck,
                add_action=AddAction.ADD_TO_HEAD,
                target_node=g_main,
                out=int(mix_bus),
                send_rev=int(rev_bus),
                send_del=int(del_bus),
                freq=freq,
                sustain=rng.uniform(0.10, 0.35),
                amp=amp,
                bright=0.55,
            )

        schedule_pattern(score, start, end, beat / 2, add_pluck)

    def schedule_lead(start, end, amp=0.11):
        melody = [12, 15, 19, 17, 12, 10, 7, 10]

        def add_lead(time):
            beat_index = int(time / beat)
            freq = midi_to_hz(prog_root_at(beat_index) + melody[beat_index % len(melody)])
            score.add_synth(
                lead,
                add_action=AddAction.ADD_TO_HEAD,
                target_node=g_main,
                out=int(mix_bus),
                send_rev=int(rev_bus),
                send_del=int(del_bus),
                freq=freq,
                sustain=0.22,
                amp=amp,
                bright=0.85,
                bite=0.55,
            )

        schedule_pattern(score, start, end, beat / 2, add_lead)

    def schedule_glitch(start, end, amp=0.05):
        def add_glitch(time):
            score.add_synth(
                glitch_hit,
                add_action=AddAction.ADD_TO_HEAD,
                target_node=g_main,
                out=int(mix_bus),
                send_rev=int(rev_bus),
                send_del=int(del_bus),
                freq=rng.uniform(300, 5200),
                dur=rng.uniform(0.03, 0.11),
                amp=rng.uniform(0.02, amp),
                crush=rng.uniform(0.35, 0.85),
                pan=rng.uniform(-0.9, 0.9),
            )

        schedule_pattern(score, start, end, beat / 2, add_glitch)

    def schedule_modem(start, end, amp=0.06):
        def add_modem(time):
            score.add_synth(
                modem,
                add_action=AddAction.ADD_TO_HEAD,
                target_node=g_main,
                out=int(mix_bus),
                send_rev=int(rev_bus),
                send_del=int(del_bus),
                dur=rng.uniform(0.12, 0.7),
                amp=rng.uniform(0.01, amp),
                pan=rng.uniform(-0.7, 0.7),
            )

        schedule_pattern(score, start, end, beat * rng.choice([1, 2, 4]), add_modem)

    def schedule_riser(start, end, amp=0.10):
        def add_riser(time):
            score.add_synth(
                riser,
                add_action=AddAction.ADD_TO_HEAD,
                target_node=g_main,
                out=int(mix_bus),
                send_rev=int(rev_bus),
                send_del=int(del_bus),
                amp=amp,
                dur=rng.uniform(2.5, 5.5),
            )

        schedule_pattern(score, start, end, beat * 8, add_riser)

    def schedule_swarm(start, end, amp=0.075):
        def add_swarm(time):
            beat_index = int(time / beat)
            freq = midi_to_hz(prog_root_at(beat_index) - 12)
            score.add_synth(
                swarm,
                add_action=AddAction.ADD_TO_HEAD,
                target_node=g_main,
                out=int(mix_bus),
                send_rev=int(rev_bus),
                send_del=int(del_bus),
                base=freq,
                life=rng.uniform(6, 14),
                amp=amp,
                chaos=rng.uniform(0.35, 0.95),
            )

        schedule_pattern(score, start, end, beat * 4, add_swarm)

    # Timeline (seconds)
    intro_end = 30.0
    build_end = 90.0
    pre_drop_end = 120.0
    drop_end = 150.0
    outro_end = 180.0

    schedule_pad(0.0, outro_end)
    schedule_bass(0.0, outro_end, amp=0.10, bright=0.10, drive=1.2)
    schedule_modem(0.0, outro_end, amp=0.07)

    schedule_kick(12.0, outro_end, amp=0.62)
    schedule_hat(30.0, drop_end, amp=0.12)
    schedule_snare(30.0, drop_end, amp=0.36)
    schedule_pluck(30.0, pre_drop_end, amp=0.08)

    schedule_glitch(90.0, outro_end, amp=0.05)
    schedule_riser(90.0, drop_end, amp=0.10)

    schedule_lead(120.0, drop_end, amp=0.11)
    schedule_swarm(120.0, drop_end, amp=0.075)

    with score.at(120.0):
        spawn_patch_cloud(
            score,
            g_patch,
            int(mix_bus),
            int(rev_bus),
            int(del_bus),
            rng,
            time=120.0,
            count=120,
            base=220,
            chaos=0.85,
            life=8,
            amp=0.010,
        )

    with score.at(150.0):
        score.add_synth(
            crash,
            add_action=AddAction.ADD_TO_HEAD,
            target_node=g_main,
            out=int(mix_bus),
            send_rev=int(rev_bus),
            send_del=int(del_bus),
            amp=0.60,
        )
        spawn_patch_cloud(
            score,
            g_patch,
            int(mix_bus),
            int(rev_bus),
            int(del_bus),
            rng,
            time=150.0,
            count=60,
            base=110,
            chaos=0.35,
            life=8,
            amp=0.007,
        )

    with score.at(outro_end):
        score.do_nothing()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    return supriya.render(score, output_file_path=output_path, header_format="wav")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render the Gatogen Anthem non-realtime cue to a WAV file"
    )
    parser.add_argument("output", type=Path, help="Output WAV file path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path, exit_code = build_score(args.output)
    if output_path:
        print(f"Rendered to {output_path}")
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
