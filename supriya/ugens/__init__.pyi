from __future__ import annotations

from .core import UGen, UGenOperable, UGenRecursiveInput
from supriya.typing import Default
from supriya.enums import DoneAction

from .basic import Mix
from .core import Check, OutputProxy, PseudoUGen, SuperColliderSynthDef, SynthDef, SynthDefBuilder, UGenSerializable, UGenVector, compile_synthdefs, decompile_synthdef, decompile_synthdefs, default, param, synthdef, ugen
from .dynamics import CompanderD
from .envelopes import Envelope
from .filters import Changed
from .lines import LinLin, Silence
from .panning import Splay
from .system import SYSTEM_SYNTHDEFS

class A2K(UGen):
    """
    An audio-rate to control-rate convert unit generator.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> a_2_k = supriya.ugens.A2K.kr(
        ...     source=source,
        ... )
        >>> a_2_k
        <A2K.kr()[0]>
    """
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class APF(UGen):
    """
    An all-pass filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> apf = supriya.ugens.APF.ar(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=source,
        ... )
        >>> apf
        <APF.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, radius: UGenRecursiveInput = 0.8) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, radius: UGenRecursiveInput = 0.8) -> UGenOperable: ...
class AllpassC(UGen):
    """
    A cubic-interpolating allpass delay line unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> allpass_c = supriya.ugens.AllpassC.ar(source=source)
        >>> allpass_c
        <AllpassC.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class AllpassL(UGen):
    """
    A linear interpolating allpass delay line unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> allpass_l = supriya.ugens.AllpassL.ar(source=source)
        >>> allpass_l
        <AllpassL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class AllpassN(UGen):
    """
    A non-interpolating allpass delay line unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> allpass_n = supriya.ugens.AllpassN.ar(source=source)
        >>> allpass_n
        <AllpassN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class AmpComp(UGen):
    """
    Basic psychoacoustic amplitude compensation.
    
    ::
    
        >>> amp_comp = supriya.ugens.AmpComp.ar(
        ...     exp=0.3333,
        ...     frequency=1000,
        ...     root=0,
        ... )
        >>> amp_comp
        <AmpComp.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 1000.0, root: UGenRecursiveInput = 0.0, exp: UGenRecursiveInput = 0.3333) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 1000.0, root: UGenRecursiveInput = 0.0, exp: UGenRecursiveInput = 0.3333) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, frequency: UGenRecursiveInput = 1000.0, root: UGenRecursiveInput = 0.0, exp: UGenRecursiveInput = 0.3333) -> UGenOperable: ...
class AmpCompA(UGen):
    """
    Basic psychoacoustic amplitude compensation (ANSI A-weighting curve).
    
    ::
    
        >>> amp_comp_a = supriya.ugens.AmpCompA.ar(
        ...     frequency=1000,
        ...     min_amp=0.32,
        ...     root=0,
        ...     root_amp=1,
        ... )
        >>> amp_comp_a
        <AmpCompA.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 1000.0, root: UGenRecursiveInput = 0.0, min_amp: UGenRecursiveInput = 0.32, root_amp: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 1000.0, root: UGenRecursiveInput = 0.0, min_amp: UGenRecursiveInput = 0.32, root_amp: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, frequency: UGenRecursiveInput = 1000.0, root: UGenRecursiveInput = 0.0, min_amp: UGenRecursiveInput = 0.32, root_amp: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class Amplitude(UGen):
    """
    An amplitude follower.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> amplitude = supriya.ugens.Amplitude.kr(
        ...     attack_time=0.01,
        ...     release_time=0.01,
        ...     source=source,
        ... )
        >>> amplitude
        <Amplitude.kr()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, attack_time: UGenRecursiveInput = 0.01, release_time: UGenRecursiveInput = 0.01) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, attack_time: UGenRecursiveInput = 0.01, release_time: UGenRecursiveInput = 0.01) -> UGenOperable: ...
class AudioControl(UGen):
    """
    A UGen: a "unit generator".
    """
    ...
class BAllPass(UGen):
    """
    An all-pass filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> ball_pass = supriya.ugens.BAllPass.ar(
        ...     frequency=1200,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> ball_pass
        <BAllPass.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 1200.0, reciprocal_of_q: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BBandPass(UGen):
    """
    A band-pass filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bband_pass = supriya.ugens.BBandPass.ar(
        ...     bandwidth=1,
        ...     frequency=1200,
        ...     source=source,
        ... )
        >>> bband_pass
        <BBandPass.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 1200.0, bandwidth: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BBandStop(UGen):
    """
    A band-stop filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bband_stop = supriya.ugens.BBandStop.ar(
        ...     bandwidth=1,
        ...     frequency=1200,
        ...     source=source,
        ... )
        >>> bband_stop
        <BBandStop.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 1200.0, bandwidth: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BHiCut(UGen):
    """
    A high-cut filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bhi_cut = supriya.ugens.BHiCut.ar(
        ...     frequency=1200,
        ...     max_order=5,
        ...     order=2,
        ...     source=source,
        ... )
        >>> bhi_cut
        <BHiCut.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 1200.0, order: UGenRecursiveInput = 2.0, max_order: UGenRecursiveInput = 5.0) -> UGenOperable: ...
class BHiPass(UGen):
    """
    A high-pass filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bhi_pass = supriya.ugens.BHiPass.ar(
        ...     frequency=1200,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> bhi_pass
        <BHiPass.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 1200.0, reciprocal_of_q: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BHiShelf(UGen):
    """
    A high-shelf filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bhi_shelf = supriya.ugens.BHiShelf.ar(
        ...     gain=0,
        ...     frequency=1200,
        ...     reciprocal_of_s=1,
        ...     source=source,
        ... )
        >>> bhi_shelf
        <BHiShelf.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 1200.0, reciprocal_of_s: UGenRecursiveInput = 1.0, gain: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class BLowCut(UGen):
    """
    A low-cut filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> blow_cut = supriya.ugens.BLowCut.ar(
        ...     frequency=1200,
        ...     max_order=5,
        ...     order=2,
        ...     source=source,
        ... )
        >>> blow_cut
        <BLowCut.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 1200.0, order: UGenRecursiveInput = 2.0, max_order: UGenRecursiveInput = 5.0) -> UGenOperable: ...
class BLowPass(UGen):
    """
    A low-pass filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> blow_pass = supriya.ugens.BLowPass.ar(
        ...     frequency=1200,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> blow_pass
        <BLowPass.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 1200.0, reciprocal_of_q: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BLowShelf(UGen):
    """
    A low-shelf filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> blow_shelf = supriya.ugens.BLowShelf.ar(
        ...     frequency=1200,
        ...     gain=0,
        ...     reciprocal_of_s=1,
        ...     source=source,
        ... )
        >>> blow_shelf
        <BLowShelf.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 1200.0, reciprocal_of_s: UGenRecursiveInput = 1.0, gain: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class BPF(UGen):
    """
    A 2nd order Butterworth bandpass filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> b_p_f = supriya.ugens.BPF.ar(source=source)
        >>> b_p_f
        <BPF.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, reciprocal_of_q: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, reciprocal_of_q: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BPZ2(UGen):
    """
    A two zero fixed midpass filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bpz_2 = supriya.ugens.BPZ2.ar(
        ...     source=source,
        ... )
        >>> bpz_2
        <BPZ2.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class BPeakEQ(UGen):
    """
    A parametric equalizer.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bpeak_eq = supriya.ugens.BPeakEQ.ar(
        ...     frequency=1200,
        ...     gain=0,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> bpeak_eq
        <BPeakEQ.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 1200.0, reciprocal_of_q: UGenRecursiveInput = 1.0, gain: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class BRF(UGen):
    """
    A 2nd order Butterworth band-reject filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> b_r_f = supriya.ugens.BRF.ar(source=source)
        >>> b_r_f
        <BRF.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, reciprocal_of_q: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, reciprocal_of_q: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BRZ2(UGen):
    """
    A two zero fixed midcut filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> brz_2 = supriya.ugens.BRZ2.ar(
        ...     source=source,
        ... )
        >>> brz_2
        <BRZ2.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class Balance2(UGen):
    """
    A stereo signal balancer.
    
    ::
    
        >>> left = supriya.ugens.WhiteNoise.ar()
        >>> right = supriya.ugens.SinOsc.ar()
        >>> balance_2 = supriya.ugens.Balance2.ar(
        ...     left=left,
        ...     level=1,
        ...     position=0,
        ...     right=right,
        ... )
        >>> balance_2
        <Balance2.ar()>
    """
    @classmethod
    def ar(cls, *, left: UGenRecursiveInput, right: UGenRecursiveInput, position: UGenRecursiveInput = 0.0, level: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, left: UGenRecursiveInput, right: UGenRecursiveInput, position: UGenRecursiveInput = 0.0, level: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class Ball(UGen):
    """
    A bouncing ball physical model.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> ball = supriya.ugens.Ball.ar(
        ...     damping=0,
        ...     friction=0.01,
        ...     gravity=1,
        ...     source=source,
        ... )
        >>> ball
        <Ball.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, gravity: UGenRecursiveInput = 1.0, damping: UGenRecursiveInput = 0.0, friction: UGenRecursiveInput = 0.01) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, gravity: UGenRecursiveInput = 1.0, damping: UGenRecursiveInput = 0.0, friction: UGenRecursiveInput = 0.01) -> UGenOperable: ...
class BeatTrack(UGen):
    """
    Autocorrelation beat tracker.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> beat_track = supriya.ugens.BeatTrack.kr(
        ...     pv_chain=pv_chain,
        ...     lock=0,
        ... )
        >>> beat_track
        <BeatTrack.kr()>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, lock: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class BeatTrack2(UGen):
    """
    A template-matching beat-tracker.
    
    ::
    
        >>> beat_track_2 = supriya.ugens.BeatTrack2.kr(
        ...     bus_index=0,
        ...     lock=False,
        ...     feature_count=4,
        ...     phase_accuracy=0.02,
        ...     weighting_scheme=-2.1,
        ...     window_size=2,
        ... )
        >>> beat_track_2
        <BeatTrack2.kr()>
    """
    @classmethod
    def kr(cls, *, bus_index: UGenRecursiveInput = 0.0, feature_count: UGenRecursiveInput, window_size: UGenRecursiveInput = 2, phase_accuracy: UGenRecursiveInput = 0.02, lock: UGenRecursiveInput = 0.0, weighting_scheme: UGenRecursiveInput = -2.1) -> UGenOperable: ...
class BiPanB2(UGen):
    """
    A 2D ambisonic b-format panner.
    
    ::
    
        >>> in_a = supriya.ugens.SinOsc.ar()
        >>> in_b = supriya.ugens.WhiteNoise.ar()
        >>> bi_pan_b_2 = supriya.ugens.BiPanB2.ar(
        ...     azimuth=-0.5,
        ...     gain=1,
        ...     in_a=in_a,
        ...     in_b=in_b,
        ... )
        >>> bi_pan_b_2
        <BiPanB2.ar()>
    
    ::
    
        >>> w, x, y = bi_pan_b_2
    """
    @classmethod
    def ar(cls, *, in_a: UGenRecursiveInput, in_b: UGenRecursiveInput, azimuth: UGenRecursiveInput, gain: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, in_a: UGenRecursiveInput, in_b: UGenRecursiveInput, azimuth: UGenRecursiveInput, gain: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BinaryOpUGen(UGen):
    """
    A UGen: a "unit generator".
    """
    ...
class Blip(UGen):
    """
    A band limited impulse generator.
    
    ::
    
        >>> blip = supriya.ugens.Blip.ar(
        ...     frequency=440,
        ...     harmonic_count=200,
        ... )
        >>> blip
        <Blip.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 440.0, harmonic_count: UGenRecursiveInput = 200.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 440.0, harmonic_count: UGenRecursiveInput = 200.0) -> UGenOperable: ...
class BlockSize(UGen):
    """
    A block size info unit generator.
    
    ::
    
        >>> supriya.ugens.BlockSize.ir()
        <BlockSize.ir()[0]>
    """
    @classmethod
    def ir(cls) -> UGenOperable: ...
class BrownNoise(UGen):
    """
    A brown noise unit generator.
    
    ::
    
        >>> supriya.ugens.BrownNoise.ar()
        <BrownNoise.ar()[0]>
    """
    @classmethod
    def ar(cls) -> UGenOperable: ...
    @classmethod
    def kr(cls) -> UGenOperable: ...
class BufAllpassC(UGen):
    """
    A buffer-based cubic-interpolating allpass delay line unit generator.
    
    ::
    
        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufAllpassC.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufAllpassC.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BufAllpassL(UGen):
    """
    A buffer-based linear-interpolating allpass delay line unit generator.
    
    ::
    
        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufAllpassL.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufAllpassL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BufAllpassN(UGen):
    """
    A buffer-based non-interpolating allpass delay line unit generator.
    
    ::
    
        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufAllpassN.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufAllpassN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BufChannels(UGen):
    """
    A buffer channel count info unit generator.
    
    ::
    
        >>> supriya.ugens.BufChannels.kr(buffer_id=0)
        <BufChannels.kr()[0]>
    """
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
class BufCombC(UGen):
    """
    A buffer-based cubic-interpolating comb delay line unit generator.
    
    ::
    
        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufCombC.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufCombC.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BufCombL(UGen):
    """
    A buffer-based linear-interpolating comb delay line unit generator.
    
    ::
    
        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufCombL.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufCombL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BufCombN(UGen):
    """
    A buffer-based non-interpolating comb delay line unit generator.
    
    ::
    
        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufCombN.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufCombN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class BufDelayC(UGen):
    """
    A buffer-based cubic-interpolating delay line unit generator.
    
    ::
    
        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufDelayC.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufDelayC.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2) -> UGenOperable: ...
class BufDelayL(UGen):
    """
    A buffer-based linear-interpolating delay line unit generator.
    
    ::
    
        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufDelayL.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufDelayL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2) -> UGenOperable: ...
class BufDelayN(UGen):
    """
    A buffer-based non-interpolating delay line unit generator.
    
    ::
    
        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufDelayN.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufDelayN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2) -> UGenOperable: ...
class BufDur(UGen):
    """
    A buffer duration info unit generator.
    
    ::
    
        >>> supriya.ugens.BufDur.kr(buffer_id=0)
        <BufDur.kr()[0]>
    """
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
class BufFrames(UGen):
    """
    A buffer frame count info unit generator.
    
    ::
    
        >>> supriya.ugens.BufFrames.kr(buffer_id=0)
        <BufFrames.kr()[0]>
    """
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
class BufRateScale(UGen):
    """
    A buffer sample-rate scale info unit generator.
    
    ::
    
        >>> supriya.ugens.BufRateScale.kr(buffer_id=0)
        <BufRateScale.kr()[0]>
    """
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
class BufRd(UGen):
    """
    A buffer-reading oscillator.
    
    ::
    
        >>> buffer_id = 23
        >>> phase = supriya.ugens.Phasor.ar(
        ...     rate=supriya.ugens.BufRateScale.kr(buffer_id=buffer_id),
        ...     start=0,
        ...     stop=supriya.ugens.BufFrames.kr(buffer_id=buffer_id),
        ... )
        >>> buf_rd = supriya.ugens.BufRd.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     interpolation=2,
        ...     loop=1,
        ...     phase=phase,
        ... )
        >>> buf_rd
        <BufRd.ar()>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, phase: UGenRecursiveInput = 0.0, loop: UGenRecursiveInput = 1, interpolation: UGenRecursiveInput = 2, channel_count: int = 1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, phase: UGenRecursiveInput = 0.0, loop: UGenRecursiveInput = 1, interpolation: UGenRecursiveInput = 2, channel_count: int = 1) -> UGenOperable: ...
class BufSampleRate(UGen):
    """
    A buffer sample-rate info unit generator.
    
    ::
    
        >>> supriya.ugens.BufSampleRate.kr(buffer_id=0)
        <BufSampleRate.kr()[0]>
    """
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
class BufSamples(UGen):
    """
    A buffer sample count info unit generator.
    
    ::
    
        >>> supriya.ugens.BufSamples.kr(buffer_id=0)
        <BufSamples.kr()[0]>
    """
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
class BufWr(UGen):
    """
    A buffer-writing oscillator.
    
    ::
    
        >>> buffer_id = 23
        >>> phase = supriya.ugens.Phasor.ar(
        ...     rate=supriya.ugens.BufRateScale.kr(buffer_id=buffer_id),
        ...     start=0,
        ...     stop=supriya.ugens.BufFrames.kr(buffer_id=buffer_id),
        ... )
        >>> source = supriya.ugens.In.ar(bus=0, channel_count=2)
        >>> buf_wr = supriya.ugens.BufWr.ar(
        ...     buffer_id=buffer_id,
        ...     loop=1,
        ...     phase=phase,
        ...     source=source,
        ... )
        >>> buf_wr
        <BufWr.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, phase: UGenRecursiveInput = 0.0, loop: UGenRecursiveInput = 1.0, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, phase: UGenRecursiveInput = 0.0, loop: UGenRecursiveInput = 1.0, source: UGenRecursiveInput) -> UGenOperable: ...
class COsc(UGen):
    """
    A chorusing wavetable oscillator.
    
    ::
    
        >>> cosc = supriya.ugens.COsc.ar(
        ...     beats=0.5,
        ...     buffer_id=23,
        ...     frequency=440,
        ... )
        >>> cosc
        <COsc.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, beats: UGenRecursiveInput = 0.5) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, beats: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class CheckBadValues(UGen):
    """
    Tests for infinity, not-a-number, and denormals.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> ugen_id = 23
        >>> post_mode = 0
        >>> check_bad_values = supriya.ugens.CheckBadValues.ar(
        ...     source=source,
        ...     ugen_id=ugen_id,
        ...     post_mode=post_mode,
        ... )
        >>> check_bad_values
        <CheckBadValues.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, ugen_id: UGenRecursiveInput = 0, post_mode: UGenRecursiveInput = 2) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, ugen_id: UGenRecursiveInput = 0, post_mode: UGenRecursiveInput = 2) -> UGenOperable: ...
class ClearBuf(UGen):
    """
    ::
    
        >>> clear_buf = supriya.ugens.ClearBuf.ir(
        ...     buffer_id=23,
        ... )
        >>> clear_buf
        <ClearBuf.ir()[0]>
    """
    @classmethod
    def ir(cls, *, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
class Clip(UGen):
    """
    Clips a signal outside given thresholds.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> clip = supriya.ugens.Clip.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ... )
        >>> clip
        <Clip.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class ClipNoise(UGen):
    """
    A clipped noise unit generator.
    
    ::
    
        >>> supriya.ugens.ClipNoise.ar()
        <ClipNoise.ar()[0]>
    """
    @classmethod
    def ar(cls) -> UGenOperable: ...
    @classmethod
    def kr(cls) -> UGenOperable: ...
class CoinGate(UGen):
    """
    A probabilistic trigger gate.
    
    ::
    
        >>> trigger = supriya.ugens.Impulse.ar()
        >>> coin_gate = supriya.ugens.CoinGate.ar(
        ...     probability=0.5,
        ...     trigger=trigger,
        ... )
        >>> coin_gate
        <CoinGate.ar()[0]>
    """
    @classmethod
    def ar(cls, *, probability: UGenRecursiveInput = 0.5, trigger: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, probability: UGenRecursiveInput = 0.5, trigger: UGenRecursiveInput) -> UGenOperable: ...
class CombC(UGen):
    """
    A cubic-interpolating comb delay line unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.CombC.ar(source=source)
        <CombC.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class CombL(UGen):
    """
    A linear interpolating comb delay line unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.CombL.ar(source=source)
        <CombL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class CombN(UGen):
    """
    A non-interpolating comb delay line unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.CombN.ar(source=source)
        <CombN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class Compander(UGen):
    """
    A general purpose hard-knee dynamics processor.
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, control: UGenRecursiveInput = 0.0, threshold: UGenRecursiveInput = 0.5, slope_below: UGenRecursiveInput = 1.0, slope_above: UGenRecursiveInput = 1.0, clamp_time: UGenRecursiveInput = 0.01, relax_time: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class Control(UGen):
    """
    A UGen: a "unit generator".
    """
    ...
class ControlDur(UGen):
    """
    A control duration info unit generator.
    
    ::
    
        >>> supriya.ugens.ControlDur.ir()
        <ControlDur.ir()[0]>
    """
    @classmethod
    def ir(cls) -> UGenOperable: ...
class ControlRate(UGen):
    """
    A control rate info unit generator.
    
    ::
    
        >>> supriya.ugens.ControlRate.ir()
        <ControlRate.ir()[0]>
    """
    @classmethod
    def ir(cls) -> UGenOperable: ...
class Convolution(UGen):
    """
    A real-time convolver.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000])
        ...     * supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ... )
        >>> convolution = supriya.ugens.Convolution.ar(
        ...     framesize=512,
        ...     kernel=kernel,
        ...     source=source,
        ... )
        >>> convolution
        <Convolution.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, kernel: UGenRecursiveInput, framesize: UGenRecursiveInput = 512) -> UGenOperable: ...
class Convolution2(UGen):
    """
    Strict convolution with fixed kernel which can be updated using a trigger signal.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000])
        ...     * supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ... )
        >>> convolution_2 = supriya.ugens.Convolution2.ar(
        ...     framesize=2048,
        ...     kernel=kernel,
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> convolution_2
        <Convolution2.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, kernel: UGenRecursiveInput, trigger: UGenRecursiveInput = 0.0, framesize: UGenRecursiveInput = 2048) -> UGenOperable: ...
class Convolution2L(UGen):
    """
    Strict convolution with fixed kernel which can be updated using a trigger signal.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000])
        ...     * supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ... )
        >>> convolution_2_l = supriya.ugens.Convolution2L.ar(
        ...     crossfade=1,
        ...     framesize=2048,
        ...     kernel=kernel,
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> convolution_2_l
        <Convolution2L.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, kernel: UGenRecursiveInput, trigger: UGenRecursiveInput = 0.0, framesize: UGenRecursiveInput = 2048, crossfade: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class Convolution3(UGen):
    """
    Strict convolution with fixed kernel which can be updated using a trigger signal.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000])
        ...     * supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ... )
        >>> convolution_3 = supriya.ugens.Convolution3.ar(
        ...     framesize=2048,
        ...     kernel=kernel,
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> convolution_3
        <Convolution3.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, kernel: UGenRecursiveInput, trigger: UGenRecursiveInput = 0.0, framesize: UGenRecursiveInput = 2048) -> UGenOperable: ...
class Crackle(UGen):
    """
    A chaotic noise generator.
    
    ::
    
        >>> crackle = supriya.ugens.Crackle.ar(
        ...     chaos_parameter=1.25,
        ... )
        >>> crackle
        <Crackle.ar()[0]>
    """
    @classmethod
    def ar(cls, *, chaos_parameter: UGenRecursiveInput = 1.5) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, chaos_parameter: UGenRecursiveInput = 1.5) -> UGenOperable: ...
class CuspL(UGen):
    """
    A linear-interpolating cusp map chaotic generator.
    
    ::
    
        >>> cusp_l = supriya.ugens.CuspL.ar(
        ...     a=1,
        ...     b=1.9,
        ...     frequency=22050,
        ...     xi=0,
        ... )
        >>> cusp_l
        <CuspL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1.0, b: UGenRecursiveInput = 1.9, xi: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class CuspN(UGen):
    """
    A non-interpolating cusp map chaotic generator.
    
    ::
    
        >>> cusp_n = supriya.ugens.CuspN.ar(
        ...     a=1,
        ...     b=1.9,
        ...     frequency=22050,
        ...     xi=0,
        ... )
        >>> cusp_n
        <CuspN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1.0, b: UGenRecursiveInput = 1.9, xi: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class DC(UGen):
    """
    A DC unit generator.
    
    ::
    
        >>> supriya.ugens.DC.ar(
        ...     source=0,
        ... )
        <DC.ar()[0]>
    
    ::
    
        >>> supriya.ugens.DC.ar(
        ...     source=(1, 2, 3),
        ... )
        <UGenVector([<DC.ar()[0]>, <DC.ar()[0]>, <DC.ar()[0]>])>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class Dbrown(UGen):
    """
    A demand-rate brownian movement generator.
    
    ::
    
        >>> dbrown = supriya.ugens.Dbrown.dr(
        ...     length=float("inf"),
        ...     maximum=1,
        ...     minimum=0,
        ...     step=0.01,
        ... )
        >>> dbrown
        <Dbrown.dr()[0]>
    """
    @classmethod
    def dr(cls, *, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0, step: UGenRecursiveInput = 0.01, length: UGenRecursiveInput = float("inf")) -> UGenOperable: ...
class Dbufrd(UGen):
    """
    A buffer-reading demand-rate UGen.
    
    ::
    
        >>> dbufrd = supriya.ugens.Dbufrd.dr(
        ...     buffer_id=0,
        ...     loop=1,
        ...     phase=0,
        ... )
        >>> dbufrd
        <Dbufrd.dr()[0]>
    """
    @classmethod
    def dr(cls, *, buffer_id: UGenRecursiveInput = 0, phase: UGenRecursiveInput = 0, loop: UGenRecursiveInput = 1) -> UGenOperable: ...
class Dbufwr(UGen):
    """
    A buffer-writing demand-rate UGen.
    
    ::
    
        >>> dbufwr = supriya.ugens.Dbufwr.dr(
        ...     buffer_id=0,
        ...     source=0,
        ...     loop=1,
        ...     phase=0,
        ... )
        >>> dbufwr
        <Dbufwr.dr()[0]>
    """
    @classmethod
    def dr(cls, *, source: UGenRecursiveInput = 0.0, buffer_id: UGenRecursiveInput = 0.0, phase: UGenRecursiveInput = 0.0, loop: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class Decay(UGen):
    """
    A leaky signal integrator.
    
    ::
    
        >>> source = supriya.ugens.Impulse.ar()
        >>> decay = supriya.ugens.Decay.ar(
        ...     source=source,
        ... )
        >>> decay
        <Decay.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class Decay2(UGen):
    """
    A leaky signal integrator.
    
    ::
    
        >>> source = supriya.ugens.Impulse.ar()
        >>> decay_2 = supriya.ugens.Decay2.ar(
        ...     source=source,
        ... )
        >>> decay_2
        <Decay2.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, attack_time: UGenRecursiveInput = 0.01, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, attack_time: UGenRecursiveInput = 0.01, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class DecodeB2(UGen):
    """
    A 2D Ambisonic B-format decoder.
    
    ::
    
        >>> source = supriya.ugens.PinkNoise.ar()
        >>> w, x, y = supriya.ugens.PanB2.ar(
        ...     source=source,
        ...     azimuth=supriya.ugens.SinOsc.kr(),
        ... )
        >>> decode_b_2 = supriya.ugens.DecodeB2.ar(
        ...     channel_count=4,
        ...     orientation=0.5,
        ...     w=w,
        ...     x=x,
        ...     y=y,
        ... )
        >>> decode_b_2
        <DecodeB2.ar()>
    """
    @classmethod
    def ar(cls, *, w: UGenRecursiveInput, x: UGenRecursiveInput, y: UGenRecursiveInput, orientation: UGenRecursiveInput = 0.5, channel_count: int = 4) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, w: UGenRecursiveInput, x: UGenRecursiveInput, y: UGenRecursiveInput, orientation: UGenRecursiveInput = 0.5, channel_count: int = 4) -> UGenOperable: ...
class DegreeToKey(UGen):
    """
    A signal-to-modal-pitch converter.`
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> degree_to_key = supriya.ugens.DegreeToKey.ar(
        ...     buffer_id=23,
        ...     octave=12,
        ...     source=source,
        ... )
        >>> degree_to_key
        <DegreeToKey.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, octave: UGenRecursiveInput = 12) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput, octave: UGenRecursiveInput = 12) -> UGenOperable: ...
class DelTapRd(UGen):
    """
    A delay tap reader unit generator.
    
    ::
    
        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> tapin = supriya.ugens.DelTapWr.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
    
    ::
    
        >>> tapin
        <DelTapWr.ar()[0]>
    
    ::
    
        >>> tapout = supriya.ugens.DelTapRd.ar(
        ...     buffer_id=buffer_id,
        ...     phase=tapin,
        ...     delay_time=0.1,
        ...     interpolation=True,
        ... )
    
    ::
    
        >>> tapout
        <DelTapRd.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, phase: UGenRecursiveInput, delay_time: UGenRecursiveInput = 0.0, interpolation: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, phase: UGenRecursiveInput, delay_time: UGenRecursiveInput = 0.0, interpolation: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class DelTapWr(UGen):
    """
    A delay tap writer unit generator.
    
    ::
    
        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> tapin = supriya.ugens.DelTapWr.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
    
    ::
    
        >>> tapin
        <DelTapWr.ar()[0]>
    
    ::
    
        >>> tapout = supriya.ugens.DelTapRd.ar(
        ...     buffer_id=buffer_id,
        ...     phase=tapin,
        ...     delay_time=0.1,
        ...     interpolation=True,
        ... )
    
    ::
    
        >>> tapout
        <DelTapRd.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput) -> UGenOperable: ...
class Delay1(UGen):
    """
    A one-sample delay line unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.Delay1.ar(source=source)
        <Delay1.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class Delay2(UGen):
    """
    A two-sample delay line unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.Delay2.ar(source=source)
        <Delay2.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class DelayC(UGen):
    """
    A cubic-interpolating delay line unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.DelayC.ar(source=source)
        <DelayC.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2) -> UGenOperable: ...
class DelayL(UGen):
    """
    A linear-interpolating delay line unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.DelayL.ar(source=source)
        <DelayL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2) -> UGenOperable: ...
class DelayN(UGen):
    """
    A non-interpolating delay line unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.DelayN.ar(source=source)
        <DelayN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2) -> UGenOperable: ...
class Demand(UGen):
    """
    Demands results from demand-rate UGens.
    
    ::
    
        >>> source = [
        ...     supriya.ugens.Dseries.dr(),
        ...     supriya.ugens.Dwhite.dr(),
        ... ]
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
        >>> demand = supriya.ugens.Demand.ar(
        ...     reset=0,
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> demand
        <Demand.ar()>
    """
    @classmethod
    def ar(cls, *, trigger: UGenRecursiveInput = 0, reset: UGenRecursiveInput = 0, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, trigger: UGenRecursiveInput = 0, reset: UGenRecursiveInput = 0, source: UGenRecursiveInput) -> UGenOperable: ...
class DemandEnvGen(UGen):
    """
    A demand rate envelope generator.
    
    ::
    
        >>> demand_env_gen = supriya.ugens.DemandEnvGen.ar(
        ...     curve=0,
        ...     done_action=0,
        ...     duration=1,
        ...     gate=1,
        ...     level=1,
        ...     level_bias=0,
        ...     level_scale=1,
        ...     reset=1,
        ...     shape=1,
        ...     time_scale=1,
        ... )
        >>> demand_env_gen
        <DemandEnvGen.ar()[0]>
    """
    @classmethod
    def ar(cls, *, level: UGenRecursiveInput, duration: UGenRecursiveInput, shape: UGenRecursiveInput = 1, curve: UGenRecursiveInput = 0, gate: UGenRecursiveInput = 1, reset: UGenRecursiveInput = 1, level_scale: UGenRecursiveInput = 1, level_bias: UGenRecursiveInput = 0, time_scale: UGenRecursiveInput = 1, done_action: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, level: UGenRecursiveInput, duration: UGenRecursiveInput, shape: UGenRecursiveInput = 1, curve: UGenRecursiveInput = 0, gate: UGenRecursiveInput = 1, reset: UGenRecursiveInput = 1, level_scale: UGenRecursiveInput = 1, level_bias: UGenRecursiveInput = 0, time_scale: UGenRecursiveInput = 1, done_action: UGenRecursiveInput = 0) -> UGenOperable: ...
class DetectSilence(UGen):
    """
    Evaluates `done_action` when input falls below `threshold`.
    
    ::
    
        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> source *= supriya.ugens.Line.kr(start=1, stop=0)
        >>> detect_silence = supriya.ugens.DetectSilence.kr(
        ...     done_action=supriya.DoneAction.FREE_SYNTH,
        ...     source=source,
        ...     threshold=0.0001,
        ...     time=1.0,
        ... )
        >>> detect_silence
        <DetectSilence.kr()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, threshold: UGenRecursiveInput = 0.0001, time: UGenRecursiveInput = 0.1, done_action: UGenRecursiveInput = DoneAction.NOTHING) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, threshold: UGenRecursiveInput = 0.0001, time: UGenRecursiveInput = 0.1, done_action: UGenRecursiveInput = DoneAction.NOTHING) -> UGenOperable: ...
class Dgeom(UGen):
    """
    A demand-rate geometric series generator.
    
    ::
    
        >>> dgeom = supriya.ugens.Dgeom.dr(
        ...     grow=2,
        ...     length=float("inf"),
        ...     start=1,
        ... )
        >>> dgeom
        <Dgeom.dr()[0]>
    """
    @classmethod
    def dr(cls, *, start: UGenRecursiveInput = 1, grow: UGenRecursiveInput = 2, length: UGenRecursiveInput = float("inf")) -> UGenOperable: ...
class Dibrown(UGen):
    """
    An integer demand-rate brownian movement generator.
    
    ::
    
        >>> dibrown = supriya.ugens.Dibrown.dr(
        ...     length=float("inf"),
        ...     maximum=1,
        ...     minimum=0,
        ...     step=0.01,
        ... )
        >>> dibrown
        <Dibrown.dr()[0]>
    """
    @classmethod
    def dr(cls, *, minimum: UGenRecursiveInput = 0, maximum: UGenRecursiveInput = 12, step: UGenRecursiveInput = 1, length: UGenRecursiveInput = float("inf")) -> UGenOperable: ...
class DiskIn(UGen):
    """
    Streams in audio from a file.
    
    ::
    
        >>> buffer_id = 23
        >>> disk_in = supriya.ugens.DiskIn.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     loop=0,
        ... )
        >>> disk_in
        <DiskIn.ar()>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, loop: UGenRecursiveInput = 0, channel_count: int = 1) -> UGenOperable: ...
class DiskOut(UGen):
    """
    Records to a soundfile to disk.
    
    ::
    
        >>> buffer_id = 0
        >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
        >>> disk_out = supriya.ugens.DiskOut.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        >>> disk_out
        <DiskOut.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput) -> UGenOperable: ...
class Diwhite(UGen):
    """
    An integer demand-rate white noise random generator.
    
    ::
    
        >>> diwhite = supriya.ugens.Diwhite.dr(
        ...     length=float("inf"),
        ...     maximum=1,
        ...     minimum=0,
        ... )
        >>> diwhite
        <Diwhite.dr()[0]>
    """
    @classmethod
    def dr(cls, *, minimum: UGenRecursiveInput = 0, maximum: UGenRecursiveInput = 1, length: UGenRecursiveInput = float("inf")) -> UGenOperable: ...
class Done(UGen):
    """
    Triggers when `source` sets its `done` flag.
    
    ::
    
        >>> source = supriya.ugens.Line.kr()
        >>> done = supriya.ugens.Done.kr(
        ...     source=source,
        ... )
        >>> done
        <Done.kr()[0]>
    """
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class Drand(UGen):
    """
    A demand-rate random sequence generator.
    
    ::
    
        >>> sequence = (1, 2, 3)
        >>> drand = supriya.ugens.Drand.dr(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> drand
        <Drand.dr()[0]>
    """
    @classmethod
    def dr(cls, *, repeats: UGenRecursiveInput = 1, sequence: UGenRecursiveInput) -> UGenOperable: ...
class Dreset(UGen):
    """
    Resets demand-rate UGens.
    
    ::
    
        >>> source = supriya.ugens.Dseries.dr(start=0, step=2)
        >>> dreset = supriya.ugens.Dreset.dr(
        ...     reset=0,
        ...     source=source,
        ... )
        >>> dreset
        <Dreset.dr()[0]>
    """
    @classmethod
    def dr(cls, *, source: UGenRecursiveInput, reset: UGenRecursiveInput = 0) -> UGenOperable: ...
class Dseq(UGen):
    """
    A demand-rate sequence generator.
    
    ::
    
        >>> sequence = (1, 2, 3)
        >>> dseq = supriya.ugens.Dseq.dr(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> dseq
        <Dseq.dr()[0]>
    """
    @classmethod
    def dr(cls, *, repeats: UGenRecursiveInput = 1, sequence: UGenRecursiveInput) -> UGenOperable: ...
class Dser(UGen):
    """
    A demand-rate sequence generator.
    
    ::
    
        >>> sequence = (1, 2, 3)
        >>> dser = supriya.ugens.Dser.dr(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> dser
        <Dser.dr()[0]>
    """
    @classmethod
    def dr(cls, *, repeats: UGenRecursiveInput = 1, sequence: UGenRecursiveInput) -> UGenOperable: ...
class Dseries(UGen):
    """
    A demand-rate arithmetic series.
    
    ::
    
        >>> dseries = supriya.ugens.Dseries.dr(
        ...     length=float("inf"),
        ...     start=1,
        ...     step=1,
        ... )
        >>> dseries
        <Dseries.dr()[0]>
    """
    @classmethod
    def dr(cls, *, length: UGenRecursiveInput = float("inf"), start: UGenRecursiveInput = 1, step: UGenRecursiveInput = 1) -> UGenOperable: ...
class Dshuf(UGen):
    """
    A demand-rate random sequence generator.
    
    ::
    
        >>> sequence = (1, 2, 3)
        >>> dshuf = supriya.ugens.Dshuf.dr(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> dshuf
        <Dshuf.dr()[0]>
    """
    @classmethod
    def dr(cls, *, repeats: UGenRecursiveInput = 1, sequence: UGenRecursiveInput) -> UGenOperable: ...
class Dstutter(UGen):
    """
    A demand-rate input replicator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> dstutter = supriya.ugens.Dstutter.dr(
        ...     n=2,
        ...     source=source,
        ... )
        >>> dstutter
        <Dstutter.dr()[0]>
    """
    @classmethod
    def dr(cls, *, n: UGenRecursiveInput = 2, source: UGenRecursiveInput) -> UGenOperable: ...
class Dswitch(UGen):
    """
    A demand-rate generator for embedding different inputs.
    
    ::
    
        >>> index = supriya.ugens.Dseq.dr(sequence=[0, 1, 2, 1, 0])
        >>> sequence = (1.0, 2.0, 3.0)
        >>> dswitch = supriya.ugens.Dswitch.dr(
        ...     index_=index,
        ...     sequence=sequence,
        ... )
        >>> dswitch
        <Dswitch.dr()[0]>
    """
    @classmethod
    def dr(cls, *, index_: UGenRecursiveInput, sequence: UGenRecursiveInput) -> UGenOperable: ...
class Dswitch1(UGen):
    """
    A demand-rate generator for switching between inputs.
    
    ::
    
        >>> index = supriya.ugens.Dseq.dr(sequence=[0, 1, 2, 1, 0])
        >>> sequence = (1.0, 2.0, 3.0)
        >>> dswitch_1 = supriya.ugens.Dswitch1.dr(
        ...     index_=index,
        ...     sequence=sequence,
        ... )
        >>> dswitch_1
        <Dswitch1.dr()[0]>
    """
    @classmethod
    def dr(cls, *, index_: UGenRecursiveInput, sequence: UGenRecursiveInput) -> UGenOperable: ...
class Dunique(UGen):
    """
    Returns the same unique series of values for several demand streams.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> dunique = supriya.ugens.Dunique.dr(
        ...     max_buffer_size=1024,
        ...     protected=True,
        ...     source=source,
        ... )
        >>> dunique
        <Dunique.dr()[0]>
    """
    @classmethod
    def dr(cls, *, source: UGenRecursiveInput, max_buffer_size: UGenRecursiveInput = 1024, protected: UGenRecursiveInput = True) -> UGenOperable: ...
class Dust(UGen):
    """
    A unipolar random impulse generator.
    
    ::
    
        >>> dust = supriya.ugens.Dust.ar(
        ...     density=23,
        ... )
        >>> dust
        <Dust.ar()[0]>
    """
    @classmethod
    def ar(cls, *, density: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, density: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class Dust2(UGen):
    """
    A bipolar random impulse generator.
    
    ::
    
        >>> dust_2 = supriya.ugens.Dust2.ar(
        ...     density=23,
        ... )
        >>> dust_2
        <Dust2.ar()[0]>
    """
    @classmethod
    def ar(cls, *, density: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, density: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class Duty(UGen):
    """
    A value is demanded of each UGen in the list and output according to a stream of duration values.
    
    ::
    
        >>> duty = supriya.ugens.Duty.kr(
        ...     done_action=0,
        ...     duration=supriya.ugens.Drand.dr(
        ...         sequence=[0.01, 0.2, 0.4],
        ...         repeats=2,
        ...     ),
        ...     reset=0,
        ...     level=supriya.ugens.Dseq.dr(
        ...         sequence=[204, 400, 201, 502, 300, 200],
        ...         repeats=2,
        ...     ),
        ... )
        >>> duty
        <Duty.kr()[0]>
    """
    @classmethod
    def ar(cls, *, duration: UGenRecursiveInput = 1.0, reset: UGenRecursiveInput = 0.0, level: UGenRecursiveInput = 1.0, done_action: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, duration: UGenRecursiveInput = 1.0, reset: UGenRecursiveInput = 0.0, level: UGenRecursiveInput = 1.0, done_action: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class Dwhite(UGen):
    """
    A demand-rate white noise random generator.
    
    ::
    
        >>> dwhite = supriya.ugens.Dwhite.dr(
        ...     length=float("inf"),
        ...     maximum=1,
        ...     minimum=0,
        ... )
        >>> dwhite
        <Dwhite.dr()[0]>
    """
    @classmethod
    def dr(cls, *, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 0.0, length: UGenRecursiveInput = float("inf")) -> UGenOperable: ...
class Dwrand(UGen):
    """
    A demand-rate weighted random sequence generator.
    
    ::
    
        >>> sequence = [0, 1, 2, 7]
        >>> weights = [0.4, 0.4, 0.1, 0.1]
        >>> dwrand = supriya.ugens.Dwrand.dr(
        ...     repeats=1,
        ...     sequence=sequence,
        ...     weights=weights,
        ... )
        >>> dwrand
        <Dwrand.dr()[0]>
    """
    @classmethod
    def dr(cls, repeats: UGenRecursiveInput = 1, sequence: UGenRecursiveInput = None, weights: UGenRecursiveInput = None) -> UGenOperable: ...
class Dxrand(UGen):
    """
    A demand-rate random sequence generator.
    
    ::
    
        >>> sequence = (1, 2, 3)
        >>> dxrand = supriya.ugens.Dxrand.dr(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> dxrand
        <Dxrand.dr()[0]>
    """
    @classmethod
    def dr(cls, *, repeats: UGenRecursiveInput = 1, sequence: UGenRecursiveInput) -> UGenOperable: ...
class EnvGen(UGen):
    """
    An envelope generator.
    
    ::
    
        >>> from supriya.ugens import Envelope, EnvGen
        >>> EnvGen.ar(envelope=Envelope.percussive())
        <EnvGen.ar()[0]>
    """
    @classmethod
    def ar(cls, *, gate: UGenRecursiveInput = 1.0, level_scale: UGenRecursiveInput = 1.0, level_bias: UGenRecursiveInput = 0.0, time_scale: UGenRecursiveInput = 1.0, done_action: UGenRecursiveInput = 0.0, envelope: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, gate: UGenRecursiveInput = 1.0, level_scale: UGenRecursiveInput = 1.0, level_bias: UGenRecursiveInput = 0.0, time_scale: UGenRecursiveInput = 1.0, done_action: UGenRecursiveInput = 0.0, envelope: UGenRecursiveInput) -> UGenOperable: ...
class ExpRand(UGen):
    """
    An exponential random distribution.
    
    ::
    
        >>> exp_rand = supriya.ugens.ExpRand.ir()
        >>> exp_rand
        <ExpRand.ir()[0]>
    """
    @classmethod
    def ir(cls, *, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class FBSineC(UGen):
    """
    A cubic-interpolating feedback sine with chaotic phase indexing.
    
    ::
    
        >>> fbsine_c = supriya.ugens.FBSineC.ar(
        ...     a=1.1,
        ...     c=0.5,
        ...     fb=0.1,
        ...     frequency=22050,
        ...     im=1,
        ...     xi=0.1,
        ...     yi=0.1,
        ... )
        >>> fbsine_c
        <FBSineC.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, im: UGenRecursiveInput = 1.0, fb: UGenRecursiveInput = 0.1, a: UGenRecursiveInput = 1.1, c: UGenRecursiveInput = 0.5, xi: UGenRecursiveInput = 0.1, yi: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class FBSineL(UGen):
    """
    A linear-interpolating feedback sine with chaotic phase indexing.
    
    ::
    
        >>> fbsine_l = supriya.ugens.FBSineL.ar(
        ...     a=1.1,
        ...     c=0.5,
        ...     fb=0.1,
        ...     frequency=22050,
        ...     im=1,
        ...     xi=0.1,
        ...     yi=0.1,
        ... )
        >>> fbsine_l
        <FBSineL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, im: UGenRecursiveInput = 1.0, fb: UGenRecursiveInput = 0.1, a: UGenRecursiveInput = 1.1, c: UGenRecursiveInput = 0.5, xi: UGenRecursiveInput = 0.1, yi: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class FBSineN(UGen):
    """
    A non-interpolating feedback sine with chaotic phase indexing.
    
    ::
    
        >>> fbsine_n = supriya.ugens.FBSineN.ar(
        ...     a=1.1,
        ...     c=0.5,
        ...     fb=0.1,
        ...     frequency=22050,
        ...     im=1,
        ...     xi=0.1,
        ...     yi=0.1,
        ... )
        >>> fbsine_n
        <FBSineN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, im: UGenRecursiveInput = 1.0, fb: UGenRecursiveInput = 0.1, a: UGenRecursiveInput = 1.1, c: UGenRecursiveInput = 0.5, xi: UGenRecursiveInput = 0.1, yi: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class FFT(UGen):
    """
    A fast Fourier transform.
    
    ::
    
        >>> buffer_id = supriya.ugens.LocalBuf.ir(frame_count=2048)
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> fft = supriya.ugens.FFT.kr(
        ...     active=1,
        ...     buffer_id=buffer_id,
        ...     hop=0.5,
        ...     source=source,
        ...     window_size=0,
        ...     window_type=0,
        ... )
        >>> fft
        <FFT.kr()[0]>
    """
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput = Default(), source: UGenRecursiveInput, hop: UGenRecursiveInput = 0.5, window_type: UGenRecursiveInput = 0, active: UGenRecursiveInput = 1, window_size: UGenRecursiveInput = 0) -> UGenOperable: ...
class FOS(UGen):
    """
    A first order filter section.
    
    ::
    
        out(i) = (a0 * in(i)) + (a1 * in(i-1)) + (a2 * in(i-2)) + (b1 * out(i-1)) + (b2 * out(i-2))
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> fos = supriya.ugens.FOS.ar(
        ...     a_0=0,
        ...     a_1=0,
        ...     b_1=0,
        ...     source=source,
        ... )
        >>> fos
        <FOS.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, a_0: UGenRecursiveInput = 0.0, a_1: UGenRecursiveInput = 0.0, b_1: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, a_0: UGenRecursiveInput = 0.0, a_1: UGenRecursiveInput = 0.0, b_1: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class FSinOsc(UGen):
    """
    Very fast sine wave generator (2 PowerPC instructions per output sample!) implemented using a ringing filter.
    
    ::
    
        >>> fsin_osc = supriya.ugens.FSinOsc.ar(
        ...     frequency=440,
        ...     initial_phase=0,
        ... )
        >>> fsin_osc
        <FSinOsc.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class Fold(UGen):
    """
    Folds a signal outside given thresholds.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> fold = supriya.ugens.Fold.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ... )
        >>> fold
        <Fold.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class Formlet(UGen):
    """
    A FOF-like filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> formlet = supriya.ugens.Formlet.ar(
        ...     attack_time=1,
        ...     decay_time=1,
        ...     frequency=440,
        ...     source=source,
        ... )
        >>> formlet
        <Formlet.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, attack_time: UGenRecursiveInput = 1.0, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, attack_time: UGenRecursiveInput = 1.0, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class Free(UGen):
    """
    Frees the node at `node_id` when triggered by `trigger`.
    
    ::
    
        >>> node_id = 1000
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> free = supriya.ugens.Free.kr(
        ...     node_id=node_id,
        ...     trigger=trigger,
        ... )
        >>> free
        <Free.kr()[0]>
    """
    @classmethod
    def kr(cls, *, trigger: UGenRecursiveInput = 0, node_id: UGenRecursiveInput) -> UGenOperable: ...
class FreeSelf(UGen):
    """
    Frees the enclosing synth when triggered by `trigger`.
    
    ::
    
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> free_self = supriya.ugens.FreeSelf.kr(
        ...     trigger=trigger,
        ... )
        >>> free_self
        <FreeSelf.kr()[0]>
    """
    @classmethod
    def kr(cls, *, trigger: UGenRecursiveInput) -> UGenOperable: ...
class FreeSelfWhenDone(UGen):
    """
    Frees the enclosing synth when `source` sets its `done` flag.
    
    ::
    
        >>> source = supriya.ugens.Line.kr()
        >>> free_self_when_done = supriya.ugens.FreeSelfWhenDone.kr(
        ...     source=source,
        ... )
        >>> free_self_when_done
        <FreeSelfWhenDone.kr()[0]>
    """
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class FreeVerb(UGen):
    """
    A FreeVerb reverb unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.FreeVerb.ar(
        ...     source=source,
        ... )
        <FreeVerb.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, mix: UGenRecursiveInput = 0.33, room_size: UGenRecursiveInput = 0.5, damping: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class FreqShift(UGen):
    """
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> freq_shift = supriya.ugens.FreqShift.ar(
        ...     frequency=0,
        ...     phase=0,
        ...     source=source,
        ... )
        >>> freq_shift
        <FreqShift.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 0.0, phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class Gate(UGen):
    """
    Gates or holds.
    
    ::
    
        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(density=1)
        >>> gate = supriya.ugens.Gate.ar(
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> gate
        <Gate.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
class GbmanL(UGen):
    """
    A non-interpolating gingerbreadman map chaotic generator.
    
    ::
    
        >>> gbman_l = supriya.ugens.GbmanL.ar(
        ...     frequency=22050,
        ...     xi=1.2,
        ...     yi=2.1,
        ... )
        >>> gbman_l
        <GbmanL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, xi: UGenRecursiveInput = 1.2, yi: UGenRecursiveInput = 2.1) -> UGenOperable: ...
class GbmanN(UGen):
    """
    A non-interpolating gingerbreadman map chaotic generator.
    
    ::
    
        >>> gbman_n = supriya.ugens.GbmanN.ar(
        ...     frequency=22050,
        ...     xi=1.2,
        ...     yi=2.1,
        ... )
        >>> gbman_n
        <GbmanN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, xi: UGenRecursiveInput = 1.2, yi: UGenRecursiveInput = 2.1) -> UGenOperable: ...
class Gendy1(UGen):
    """
    A dynamic stochastic synthesis generator.
    
    ::
    
        >>> gendy_1 = supriya.ugens.Gendy1.ar(
        ...     adparam=1,
        ...     ampdist=1,
        ...     ampscale=0.5,
        ...     ddparam=1,
        ...     durdist=1,
        ...     durscale=0.5,
        ...     init_cps=12,
        ...     knum=10,
        ...     maxfrequency=660,
        ...     minfrequency=440,
        ... )
        >>> gendy_1
        <Gendy1.ar()[0]>
    """
    @classmethod
    def ar(cls, *, ampdist: UGenRecursiveInput = 1, durdist: UGenRecursiveInput = 1, adparam: UGenRecursiveInput = 1, ddparam: UGenRecursiveInput = 1, minfrequency: UGenRecursiveInput = 440, maxfrequency: UGenRecursiveInput = 660, ampscale: UGenRecursiveInput = 0.5, durscale: UGenRecursiveInput = 0.5, init_cps: UGenRecursiveInput = 12, knum: UGenRecursiveInput = Default()) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, ampdist: UGenRecursiveInput = 1, durdist: UGenRecursiveInput = 1, adparam: UGenRecursiveInput = 1, ddparam: UGenRecursiveInput = 1, minfrequency: UGenRecursiveInput = 440, maxfrequency: UGenRecursiveInput = 660, ampscale: UGenRecursiveInput = 0.5, durscale: UGenRecursiveInput = 0.5, init_cps: UGenRecursiveInput = 12, knum: UGenRecursiveInput = Default()) -> UGenOperable: ...
class Gendy2(UGen):
    """
    A dynamic stochastic synthesis generator.
    
    ::
    
        >>> gendy_2 = supriya.ugens.Gendy2.ar(
        ...     a=1.17,
        ...     adparam=1,
        ...     ampdist=1,
        ...     ampscale=0.5,
        ...     c=0.31,
        ...     ddparam=1,
        ...     durdist=1,
        ...     durscale=0.5,
        ...     init_cps=12,
        ...     knum=10,
        ...     maxfrequency=660,
        ...     minfrequency=440,
        ... )
        >>> gendy_2
        <Gendy2.ar()[0]>
    """
    @classmethod
    def ar(cls, *, ampdist: UGenRecursiveInput = 1, durdist: UGenRecursiveInput = 1, adparam: UGenRecursiveInput = 1, ddparam: UGenRecursiveInput = 1, minfrequency: UGenRecursiveInput = 440, maxfrequency: UGenRecursiveInput = 660, ampscale: UGenRecursiveInput = 0.5, durscale: UGenRecursiveInput = 0.5, init_cps: UGenRecursiveInput = 12, knum: UGenRecursiveInput = Default(), a: UGenRecursiveInput = 1.17, c: UGenRecursiveInput = 0.31) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, ampdist: UGenRecursiveInput = 1, durdist: UGenRecursiveInput = 1, adparam: UGenRecursiveInput = 1, ddparam: UGenRecursiveInput = 1, minfrequency: UGenRecursiveInput = 440, maxfrequency: UGenRecursiveInput = 660, ampscale: UGenRecursiveInput = 0.5, durscale: UGenRecursiveInput = 0.5, init_cps: UGenRecursiveInput = 12, knum: UGenRecursiveInput = Default(), a: UGenRecursiveInput = 1.17, c: UGenRecursiveInput = 0.31) -> UGenOperable: ...
class Gendy3(UGen):
    """
    A dynamic stochastic synthesis generator.
    
    ::
    
        >>> gendy_3 = supriya.ugens.Gendy3.ar(
        ...     adparam=1,
        ...     ampdist=1,
        ...     ampscale=0.5,
        ...     ddparam=1,
        ...     durdist=1,
        ...     durscale=0.5,
        ...     frequency=440,
        ...     init_cps=12,
        ...     knum=10,
        ... )
        >>> gendy_3
        <Gendy3.ar()[0]>
    """
    @classmethod
    def ar(cls, *, ampdist: UGenRecursiveInput = 1, durdist: UGenRecursiveInput = 1, adparam: UGenRecursiveInput = 1, ddparam: UGenRecursiveInput = 1, frequency: UGenRecursiveInput = 440, ampscale: UGenRecursiveInput = 0.5, durscale: UGenRecursiveInput = 0.5, init_cps: UGenRecursiveInput = 12, knum: UGenRecursiveInput = Default()) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, ampdist: UGenRecursiveInput = 1, durdist: UGenRecursiveInput = 1, adparam: UGenRecursiveInput = 1, ddparam: UGenRecursiveInput = 1, frequency: UGenRecursiveInput = 440, ampscale: UGenRecursiveInput = 0.5, durscale: UGenRecursiveInput = 0.5, init_cps: UGenRecursiveInput = 12, knum: UGenRecursiveInput = Default()) -> UGenOperable: ...
class GrainBuf(UGen):
    """
    ::
    
        >>> grain_buf = supriya.ugens.GrainBuf.ar(
        ...     channel_count=2,
        ...     duration=1,
        ...     envelope_buffer_id=-1,
        ...     interpolate=2,
        ...     maximum_overlap=512,
        ...     pan=0,
        ...     position=0,
        ...     rate=1,
        ...     buffer_id=0,
        ...     trigger=0,
        ... )
        >>> grain_buf
        <GrainBuf.ar()>
    """
    @classmethod
    def ar(cls, *, trigger: UGenRecursiveInput = 0, duration: UGenRecursiveInput = 1, buffer_id: UGenRecursiveInput, rate: UGenRecursiveInput = 1, position: UGenRecursiveInput = 0, interpolate: UGenRecursiveInput = 2, pan: UGenRecursiveInput = 0, envelope_buffer_id: UGenRecursiveInput = -1, maximum_overlap: UGenRecursiveInput = 512, channel_count: int = 1) -> UGenOperable: ...
class GrainIn(UGen):
    """
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> grain_in = supriya.ugens.GrainIn.ar(
        ...     channel_count=2,
        ...     duration=1,
        ...     envelope_buffer_id=-1,
        ...     maximum_overlap=512,
        ...     position=0,
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> grain_in
        <GrainIn.ar()>
    """
    @classmethod
    def ar(cls, *, trigger: UGenRecursiveInput = 0, duration: UGenRecursiveInput = 1, source: UGenRecursiveInput, position: UGenRecursiveInput = 0, envelope_buffer_id: UGenRecursiveInput = -1, maximum_overlap: UGenRecursiveInput = 512, channel_count: int = 1) -> UGenOperable: ...
class GrayNoise(UGen):
    """
    A gray noise unit generator.
    
    ::
    
        >>> supriya.ugens.GrayNoise.ar()
        <GrayNoise.ar()[0]>
    """
    @classmethod
    def ar(cls) -> UGenOperable: ...
    @classmethod
    def kr(cls) -> UGenOperable: ...
class HPF(UGen):
    """
    A Highpass filter unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.HPF.ar(source=source)
        <HPF.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0) -> UGenOperable: ...
class HPZ1(UGen):
    """
    A two point difference filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hpz_1 = supriya.ugens.HPZ1.ar(
        ...     source=source,
        ... )
        >>> hpz_1
        <HPZ1.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class HPZ2(UGen):
    """
    A two zero fixed midcut filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hpz_2 = supriya.ugens.HPZ2.ar(
        ...     source=source,
        ... )
        >>> hpz_2
        <HPZ2.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class Hasher(UGen):
    """
    A signal hasher.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> hasher = supriya.ugens.Hasher.ar(
        ...     source=source,
        ... )
        >>> hasher
        <Hasher.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class HenonC(UGen):
    """
    A cubic-interpolating henon map chaotic generator.
    
    ::
    
        >>> henon_c = supriya.ugens.HenonC.ar(
        ...     a=1.4,
        ...     b=0.3,
        ...     frequency=22050,
        ...     x_0=0,
        ...     x_1=0,
        ... )
        >>> henon_c
        <HenonC.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1.4, b: UGenRecursiveInput = 0.3, x_0: UGenRecursiveInput = 0, x_1: UGenRecursiveInput = 0) -> UGenOperable: ...
class HenonL(UGen):
    """
    A linear-interpolating henon map chaotic generator.
    
    ::
    
        >>> henon_l = supriya.ugens.HenonL.ar(
        ...     a=1.4,
        ...     b=0.3,
        ...     frequency=22050,
        ...     x_0=0,
        ...     x_1=0,
        ... )
        >>> henon_l
        <HenonL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1.4, b: UGenRecursiveInput = 0.3, x_0: UGenRecursiveInput = 0, x_1: UGenRecursiveInput = 0) -> UGenOperable: ...
class HenonN(UGen):
    """
    A non-interpolating henon map chaotic generator.
    
    ::
    
        >>> henon_n = supriya.ugens.HenonN.ar(
        ...     a=1.4,
        ...     b=0.3,
        ...     frequency=22050,
        ...     x_0=0,
        ...     x_1=0,
        ... )
        >>> henon_n
        <HenonN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1.4, b: UGenRecursiveInput = 0.3, x_0: UGenRecursiveInput = 0, x_1: UGenRecursiveInput = 0) -> UGenOperable: ...
class Hilbert(UGen):
    """
    Applies the Hilbert transform.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hilbert = supriya.ugens.Hilbert.ar(
        ...     source=source,
        ... )
        >>> hilbert
        <Hilbert.ar()>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class HilbertFIR(UGen):
    """
    Applies the Hilbert transform.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hilbert_fir = supriya.ugens.HilbertFIR.ar(
        ...     buffer_id=23,
        ...     source=source,
        ... )
        >>> hilbert_fir
        <HilbertFIR.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, buffer_id: UGenRecursiveInput) -> UGenOperable: ...
class IFFT(UGen):
    """
    An inverse fast Fourier transform.
    
    ::
    
        >>> pv_chain = supriya.ugens.LocalBuf.ir(frame_count=2048)
        >>> ifft = supriya.ugens.IFFT.ar(
        ...     pv_chain=pv_chain,
        ...     window_size=0,
        ...     window_type=0,
        ... )
        >>> ifft
        <IFFT.ar()[0]>
    """
    @classmethod
    def ar(cls, *, pv_chain: UGenRecursiveInput, window_type: UGenRecursiveInput = 0, window_size: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, window_type: UGenRecursiveInput = 0, window_size: UGenRecursiveInput = 0) -> UGenOperable: ...
class IRand(UGen):
    """
    An integer uniform random distribution.
    
    ::
    
        >>> supriya.ugens.IRand.ir()
        <IRand.ir()[0]>
    """
    @classmethod
    def ir(cls, *, minimum: UGenRecursiveInput = 0, maximum: UGenRecursiveInput = 127) -> UGenOperable: ...
class Impulse(UGen):
    """
    A non-band-limited single-sample impulse generator unit generator.
    
    ::
    
        >>> supriya.ugens.Impulse.ar()
        <Impulse.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 440.0, phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 440.0, phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class In(UGen):
    """
    A bus input unit generator.
    
    ::
    
        >>> supriya.ugens.In.ar(bus=0, channel_count=4)
        <In.ar()>
    """
    @classmethod
    def ar(cls, *, bus: UGenRecursiveInput = 0.0, channel_count: int = 1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, bus: UGenRecursiveInput = 0.0, channel_count: int = 1) -> UGenOperable: ...
class InFeedback(UGen):
    """
    A bus input unit generator.
    
    Reads signal from a bus with a current or one cycle old timestamp.
    
    ::
    
        >>> in_feedback = supriya.ugens.InFeedback.ar(
        ...     bus=0,
        ...     channel_count=2,
        ... )
        >>> in_feedback
        <InFeedback.ar()>
    """
    @classmethod
    def ar(cls, *, bus: UGenRecursiveInput = 0.0, channel_count: int = 1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, bus: UGenRecursiveInput = 0.0, channel_count: int = 1) -> UGenOperable: ...
class InRange(UGen):
    """
    Tests if a signal is within a given range.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> in_range = supriya.ugens.InRange.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ... )
        >>> in_range
        <InRange.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class Index(UGen):
    """
    A clipping buffer indexer.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> index = supriya.ugens.Index.ar(
        ...     buffer_id=23,
        ...     source=source,
        ... )
        >>> index
        <Index.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput) -> UGenOperable: ...
class Integrator(UGen):
    """
    A leaky integrator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> integrator = supriya.ugens.Integrator.ar(
        ...     coefficient=1,
        ...     source=source,
        ... )
        >>> integrator
        <Integrator.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, coefficient: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, coefficient: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class K2A(UGen):
    """
    A control-rate to audio-rate converter unit generator.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.kr()
        >>> k_2_a = supriya.ugens.K2A.ar(
        ...     source=source,
        ... )
        >>> k_2_a
        <K2A.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class KeyState(UGen):
    """
    A UGen: a "unit generator".
    """
    @classmethod
    def kr(cls, *, keycode: UGenRecursiveInput = 0.0, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0, lag: UGenRecursiveInput = 0.2) -> UGenOperable: ...
class KeyTrack(UGen):
    """
    A key tracker.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> key_track = supriya.ugens.KeyTrack.kr(
        ...     pv_chain=pv_chain,
        ...     chroma_leak=0.5,
        ...     key_decay=2,
        ... )
        >>> key_track
        <KeyTrack.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, key_decay: UGenRecursiveInput = 2, chroma_leak: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class Klank(UGen):
    """
    A bank of resonators.
    
    ::
    
        >>> klank = supriya.ugens.Klank.ar(
        ...     amplitudes=None,
        ...     decay_scale=1,
        ...     decay_times=[1, 1, 1, 1],
        ...     frequencies=[200, 671, 1153, 1723],
        ...     frequency_offset=0,
        ...     frequency_scale=1,
        ...     source=supriya.ugens.BrownNoise.ar() * 0.001,
        ... )
        >>> klank
        <Klank.ar()[0]>
    """
    @classmethod
    def ar(cls, *, amplitudes: UGenRecursiveInput = None, decay_scale: UGenRecursiveInput = 1, decay_times: UGenRecursiveInput = None, frequencies: UGenRecursiveInput, frequency_offset: UGenRecursiveInput = 0, frequency_scale: UGenRecursiveInput = 1, source: UGenRecursiveInput) -> UGenOperable: ...
class LFClipNoise(UGen):
    """
    A dynamic clipped noise generator.
    
    ::
    
        >>> supriya.ugens.LFClipNoise.ar()
        <LFClipNoise.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
class LFCub(UGen):
    """
    A sine-like oscillator unit generator.
    
    ::
    
        >>> supriya.ugens.LFCub.ar()
        <LFCub.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class LFDClipNoise(UGen):
    """
    A clipped noise generator.
    
    ::
    
        >>> supriya.ugens.LFDClipNoise.ar()
        <LFDClipNoise.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
class LFDNoise0(UGen):
    """
    A dynamic step noise generator.
    
    ::
    
        >>> supriya.ugens.LFDNoise0.ar()
        <LFDNoise0.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
class LFDNoise1(UGen):
    """
    A dynamic ramp noise generator.
    
    ::
    
        >>> supriya.ugens.LFDNoise1.ar()
        <LFDNoise1.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
class LFDNoise3(UGen):
    """
    A dynamic polynomial noise generator.
    
    ::
    
        >>> supriya.ugens.LFDNoise3.ar()
        <LFDNoise3.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
class LFGauss(UGen):
    """
    A non-band-limited gaussian function oscillator.
    
    ::
    
        >>> supriya.ugens.LFGauss.ar()
        <LFGauss.ar()[0]>
    """
    @classmethod
    def ar(cls, *, duration: UGenRecursiveInput = 1, width: UGenRecursiveInput = 0.1, initial_phase: UGenRecursiveInput = 0, loop: UGenRecursiveInput = 1, done_action: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, duration: UGenRecursiveInput = 1, width: UGenRecursiveInput = 0.1, initial_phase: UGenRecursiveInput = 0, loop: UGenRecursiveInput = 1, done_action: UGenRecursiveInput = 0) -> UGenOperable: ...
class LFNoise0(UGen):
    """
    A step noise generator.
    
    ::
    
        >>> supriya.ugens.LFNoise0.ar()
        <LFNoise0.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
class LFNoise1(UGen):
    """
    A ramp noise generator.
    
    ::
    
        >>> supriya.ugens.LFNoise1.ar()
        <LFNoise1.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
class LFNoise2(UGen):
    """
    A quadratic noise generator.
    
    ::
    
        >>> supriya.ugens.LFNoise2.ar()
        <LFNoise2.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 500.0) -> UGenOperable: ...
class LFPar(UGen):
    """
    A parabolic oscillator unit generator.
    
    ::
    
        >>> supriya.ugens.LFPar.ar()
        <LFPar.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class LFPulse(UGen):
    """
    A non-band-limited pulse oscillator.
    
    ::
    
        >>> supriya.ugens.LFPulse.ar()
        <LFPulse.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0, width: UGenRecursiveInput = 0.5) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0, width: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class LFSaw(UGen):
    """
    A non-band-limited sawtooth oscillator unit generator.
    
    ::
    
        >>> supriya.ugens.LFSaw.ar()
        <LFSaw.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class LFTri(UGen):
    """
    A non-band-limited triangle oscillator unit generator.
    
    ::
    
        >>> supriya.ugens.LFTri.ar()
        <LFTri.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class LPF(UGen):
    """
    A lowpass filter unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.LPF.ar(source=source)
        <LPF.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0) -> UGenOperable: ...
class LPZ1(UGen):
    """
    A two point average filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lpz_1 = supriya.ugens.LPZ1.ar(
        ...     source=source,
        ... )
        >>> lpz_1
        <LPZ1.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class LPZ2(UGen):
    """
    A two zero fixed lowpass filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lpz_2 = supriya.ugens.LPZ2.ar(
        ...     source=source,
        ... )
        >>> lpz_2
        <LPZ2.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class Lag(UGen):
    """
    A lag generator.
    
    ::
    
        >>> source = supriya.ugens.In.kr(bus=0)
        >>> supriya.ugens.Lag.kr(
        ...     lag_time=0.5,
        ...     source=source,
        ... )
        <Lag.kr()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, lag_time: UGenRecursiveInput = 0.1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, lag_time: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class Lag2(UGen):
    """
    An exponential lag generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lag_2 = supriya.ugens.Lag2.ar(
        ...     lag_time=0.1,
        ...     source=source,
        ... )
        >>> lag_2
        <Lag2.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, lag_time: UGenRecursiveInput = 0.1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, lag_time: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class Lag2UD(UGen):
    """
    An up/down exponential lag generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lag_2_ud = supriya.ugens.Lag2UD.ar(
        ...     lag_time_down=0.1,
        ...     lag_time_up=0.1,
        ...     source=source,
        ... )
        >>> lag_2_ud
        <Lag2UD.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, lag_time_up: UGenRecursiveInput = 0.1, lag_time_down: UGenRecursiveInput = 0.1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, lag_time_up: UGenRecursiveInput = 0.1, lag_time_down: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class Lag3(UGen):
    """
    An exponential lag generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lag_3 = supriya.ugens.Lag3.ar(
        ...     lag_time=0.1,
        ...     source=source,
        ... )
        >>> lag_3
        <Lag3.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, lag_time: UGenRecursiveInput = 0.1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, lag_time: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class Lag3UD(UGen):
    """
    An up/down exponential lag generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lag_3_ud = supriya.ugens.Lag3UD.ar(
        ...     lag_time_down=0.1,
        ...     lag_time_up=0.1,
        ...     source=source,
        ... )
        >>> lag_3_ud
        <Lag3UD.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, lag_time_up: UGenRecursiveInput = 0.1, lag_time_down: UGenRecursiveInput = 0.1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, lag_time_up: UGenRecursiveInput = 0.1, lag_time_down: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class LagControl(UGen):
    """
    A UGen: a "unit generator".
    """
    ...
class LagUD(UGen):
    """
    An up/down lag generator.
    
    ::
    
        >>> source = supriya.ugens.In.kr(bus=0)
        >>> supriya.ugens.LagUD.kr(
        ...     lag_time_down=1.25,
        ...     lag_time_up=0.5,
        ...     source=source,
        ... )
        <LagUD.kr()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, lag_time_up: UGenRecursiveInput = 0.1, lag_time_down: UGenRecursiveInput = 0.1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, lag_time_up: UGenRecursiveInput = 0.1, lag_time_down: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class Latch(UGen):
    """
    Samples and holds.
    
    ::
    
        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(density=1)
        >>> latch = supriya.ugens.Latch.ar(
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> latch
        <Latch.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
class LatoocarfianC(UGen):
    """
    A cubic-interpolating Latoocarfian chaotic generator.
    
    ::
    
        >>> latoocarfian_c = supriya.ugens.LatoocarfianC.ar(
        ...     a=1,
        ...     b=3,
        ...     c=0.5,
        ...     d=0.5,
        ...     frequency=22050,
        ...     xi=0.5,
        ...     yi=0.5,
        ... )
        >>> latoocarfian_c
        <LatoocarfianC.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1, b: UGenRecursiveInput = 3, c: UGenRecursiveInput = 0.5, d: UGenRecursiveInput = 0.5, xi: UGenRecursiveInput = 0.5, yi: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class LatoocarfianL(UGen):
    """
    A linear-interpolating Latoocarfian chaotic generator.
    
    ::
    
        >>> latoocarfian_l = supriya.ugens.LatoocarfianL.ar(
        ...     a=1,
        ...     b=3,
        ...     c=0.5,
        ...     d=0.5,
        ...     frequency=22050,
        ...     xi=0.5,
        ...     yi=0.5,
        ... )
        >>> latoocarfian_l
        <LatoocarfianL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1, b: UGenRecursiveInput = 3, c: UGenRecursiveInput = 0.5, d: UGenRecursiveInput = 0.5, xi: UGenRecursiveInput = 0.5, yi: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class LatoocarfianN(UGen):
    """
    A non-interpolating Latoocarfian chaotic generator.
    
    ::
    
        >>> latoocarfian_n = supriya.ugens.LatoocarfianN.ar(
        ...     a=1,
        ...     b=3,
        ...     c=0.5,
        ...     d=0.5,
        ...     frequency=22050,
        ...     xi=0.5,
        ...     yi=0.5,
        ... )
        >>> latoocarfian_n
        <LatoocarfianN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1, b: UGenRecursiveInput = 3, c: UGenRecursiveInput = 0.5, d: UGenRecursiveInput = 0.5, xi: UGenRecursiveInput = 0.5, yi: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class LeakDC(UGen):
    """
    A DC blocker.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> leak_d_c = supriya.ugens.LeakDC.ar(
        ...     source=source,
        ...     coefficient=0.995,
        ... )
        >>> leak_d_c
        <LeakDC.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, coefficient: UGenRecursiveInput = 0.995) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, coefficient: UGenRecursiveInput = 0.995) -> UGenOperable: ...
class LeastChange(UGen):
    """
    Outputs least changed input.
    
    ::
    
        >>> least_change = supriya.ugens.LeastChange.ar(
        ...     a=0,
        ...     b=0,
        ... )
        >>> least_change
        <LeastChange.ar()[0]>
    """
    @classmethod
    def ar(cls, *, a: UGenRecursiveInput = 0, b: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, a: UGenRecursiveInput = 0, b: UGenRecursiveInput = 0) -> UGenOperable: ...
class Limiter(UGen):
    """
    A peak limiter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> limiter = supriya.ugens.Limiter.ar(
        ...     duration=0.01,
        ...     level=1,
        ...     source=source,
        ... )
        >>> limiter
        <Limiter.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, level: UGenRecursiveInput = 1.0, duration: UGenRecursiveInput = 0.01) -> UGenOperable: ...
class LinCongC(UGen):
    """
    A cubic-interpolating linear congruential chaotic generator.
    
    ::
    
        >>> lin_cong_c = supriya.ugens.LinCongC.ar(
        ...     a=1.1,
        ...     c=0.13,
        ...     frequency=22050,
        ...     m=1,
        ...     xi=0,
        ... )
        >>> lin_cong_c
        <LinCongC.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1.1, c: UGenRecursiveInput = 0.13, m: UGenRecursiveInput = 1, xi: UGenRecursiveInput = 0) -> UGenOperable: ...
class LinCongL(UGen):
    """
    A linear-interpolating linear congruential chaotic generator.
    
    ::
    
        >>> lin_cong_l = supriya.ugens.LinCongL.ar(
        ...     a=1.1,
        ...     c=0.13,
        ...     frequency=22050,
        ...     m=1,
        ...     xi=0,
        ... )
        >>> lin_cong_l
        <LinCongL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1.1, c: UGenRecursiveInput = 0.13, m: UGenRecursiveInput = 1, xi: UGenRecursiveInput = 0) -> UGenOperable: ...
class LinCongN(UGen):
    """
    A non-interpolating linear congruential chaotic generator.
    
    ::
    
        >>> lin_cong_n = supriya.ugens.LinCongN.ar(
        ...     a=1.1,
        ...     c=0.13,
        ...     frequency=22050,
        ...     m=1,
        ...     xi=0,
        ... )
        >>> lin_cong_n
        <LinCongN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1.1, c: UGenRecursiveInput = 0.13, m: UGenRecursiveInput = 1, xi: UGenRecursiveInput = 0) -> UGenOperable: ...
class LinExp(UGen):
    """
    A linear-to-exponential range mapper.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> lin_exp = supriya.ugens.LinExp.ar(
        ...     input_maximum=1.0,
        ...     input_minimum=-1.0,
        ...     output_maximum=22050,
        ...     output_minimum=20,
        ...     source=source,
        ... )
        >>> lin_exp
        <LinExp.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, input_minimum: UGenRecursiveInput = 0, input_maximum: UGenRecursiveInput = 1, output_minimum: UGenRecursiveInput = 1, output_maximum: UGenRecursiveInput = 2) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, input_minimum: UGenRecursiveInput = 0, input_maximum: UGenRecursiveInput = 1, output_minimum: UGenRecursiveInput = 1, output_maximum: UGenRecursiveInput = 2) -> UGenOperable: ...
class LinRand(UGen):
    """
    A skewed linear random distribution.
    
    ::
    
        >>> lin_rand = supriya.ugens.LinRand.ir(
        ...     minimum=-1.0,
        ...     maximum=1.0,
        ...     skew=0.5,
        ... )
        >>> lin_rand
        <LinRand.ir()[0]>
    """
    @classmethod
    def ir(cls, *, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0, skew: UGenRecursiveInput = 0) -> UGenOperable: ...
class Line(UGen):
    """
    A line generating unit generator.
    
    ::
    
        >>> supriya.ugens.Line.ar()
        <Line.ar()[0]>
    """
    @classmethod
    def ar(cls, *, start: UGenRecursiveInput = 0.0, stop: UGenRecursiveInput = 1.0, duration: UGenRecursiveInput = 1.0, done_action: UGenRecursiveInput = DoneAction.NOTHING) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, start: UGenRecursiveInput = 0.0, stop: UGenRecursiveInput = 1.0, duration: UGenRecursiveInput = 1.0, done_action: UGenRecursiveInput = DoneAction.NOTHING) -> UGenOperable: ...
class Linen(UGen):
    """
    A simple line generating unit generator.
    
    ::
    
        >>> supriya.ugens.Linen.kr()
        <Linen.kr()[0]>
    """
    @classmethod
    def kr(cls, *, gate: UGenRecursiveInput = 1.0, attack_time: UGenRecursiveInput = 0.01, sustain_level: UGenRecursiveInput = 1.0, release_time: UGenRecursiveInput = 1.0, done_action: UGenRecursiveInput = 0) -> UGenOperable: ...
class LocalBuf(UGen):
    """
    A synth-local buffer.
    
    ::
    
        >>> from supriya.ugens import FFT, IFFT, LocalBuf, Out, PinkNoise, SynthDefBuilder
    
    ::
    
        >>> local_buf = LocalBuf.ir(
        ...     channel_count=1,
        ...     frame_count=1,
        ... )
        >>> local_buf
        <LocalBuf.ir()[0]>
    
    LocalBuf creates a ``MaxLocalBufs`` UGen implicitly during SynthDef compilation:
    
    ::
    
        >>> with SynthDefBuilder() as builder:
        ...     local_buf = LocalBuf.ir(frame_count=2048)
        ...     source = PinkNoise.ar()
        ...     pv_chain = FFT.kr(
        ...         buffer_id=local_buf,
        ...         source=source,
        ...     )
        ...     ifft = IFFT.ar(pv_chain=pv_chain)
        ...     out = Out.ar(bus=0, source=ifft)
        ...
        >>> synthdef = builder.build()
        >>> for ugen in synthdef.ugens:
        ...     ugen
        ...
        <MaxLocalBufs.ir()>
        <LocalBuf.ir()>
        <PinkNoise.ar()>
        <FFT.kr()>
        <IFFT.ar()>
        <Out.ar()>
    """
    @classmethod
    def ir(cls, *, channel_count: int = 1, frame_count: UGenRecursiveInput = 1) -> UGenOperable: ...
class LocalIn(UGen):
    """
    A SynthDef-local bus input.
    
    ::
    
        >>> supriya.ugens.LocalIn.ar(channel_count=2)
        <LocalIn.ar()>
    """
    @classmethod
    def ar(cls, *, default: UGenRecursiveInput = 0.0, channel_count: int = 1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, default: UGenRecursiveInput = 0.0, channel_count: int = 1) -> UGenOperable: ...
class LocalOut(UGen):
    """
    A SynthDef-local bus output.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.LocalOut.ar(
        ...     source=source,
        ... )
        <LocalOut.ar()>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class Logistic(UGen):
    """
    A chaotic noise function.
    
    ::
    
        >>> logistic = supriya.ugens.Logistic.ar(
        ...     chaos_parameter=3.0,
        ...     frequency=1000,
        ...     initial_y=0.5,
        ... )
        >>> logistic
        <Logistic.ar()[0]>
    """
    @classmethod
    def ar(cls, *, chaos_parameter: UGenRecursiveInput = 3, frequency: UGenRecursiveInput = 1000, initial_y: UGenRecursiveInput = 0.5) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, chaos_parameter: UGenRecursiveInput = 3, frequency: UGenRecursiveInput = 1000, initial_y: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class LorenzL(UGen):
    """
    A linear-interpolating Lorenz chaotic generator.
    
    ::
    
        >>> lorenz_l = supriya.ugens.LorenzL.ar(
        ...     b=2.667,
        ...     frequency=22050,
        ...     h=0.05,
        ...     r=28,
        ...     s=10,
        ...     xi=0.1,
        ...     yi=0,
        ...     zi=0,
        ... )
        >>> lorenz_l
        <LorenzL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, s: UGenRecursiveInput = 10, r: UGenRecursiveInput = 28, b: UGenRecursiveInput = 2.667, h: UGenRecursiveInput = 0.05, xi: UGenRecursiveInput = 0.1, yi: UGenRecursiveInput = 0, zi: UGenRecursiveInput = 0) -> UGenOperable: ...
class Loudness(UGen):
    """
    Extraction of instantaneous loudness in `sones`.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> loudness = supriya.ugens.Loudness.kr(
        ...     pv_chain=pv_chain,
        ...     smask=0.25,
        ...     tmask=1,
        ... )
        >>> loudness
        <Loudness.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, smask: UGenRecursiveInput = 0.25, tmask: UGenRecursiveInput = 1) -> UGenOperable: ...
class MFCC(UGen):
    """
    Mel frequency cepstral coefficients.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> mfcc = supriya.ugens.MFCC.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> mfcc
        <MFCC.kr()>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, coeff_count: UGenRecursiveInput = 13) -> UGenOperable: ...
class MantissaMask(UGen):
    """
    A floating-point mantissa mask.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> mantissa_mask = supriya.ugens.MantissaMask.ar(
        ...     source=source,
        ...     bits=3,
        ... )
        >>> mantissa_mask
        <MantissaMask.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput = 0, bits: UGenRecursiveInput = 3) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput = 0, bits: UGenRecursiveInput = 3) -> UGenOperable: ...
class MaxLocalBufs(UGen):
    """
    Sets the maximum number of local buffers in a synth.
    
    Used internally by LocalBuf.
    
    ::
    
        >>> max_local_bufs = supriya.ugens.MaxLocalBufs.ir(maximum=1)
        >>> max_local_bufs
        <MaxLocalBufs.ir()[0]>
    """
    @classmethod
    def ir(cls, *, maximum: UGenRecursiveInput = 0) -> UGenOperable: ...
class Median(UGen):
    """
    A median filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> median = supriya.ugens.Median.ar(
        ...     length=3,
        ...     source=source,
        ... )
        >>> median
        <Median.ar()[0]>
    """
    @classmethod
    def ar(cls, *, length: UGenRecursiveInput = 3, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, length: UGenRecursiveInput = 3, source: UGenRecursiveInput) -> UGenOperable: ...
class MidEQ(UGen):
    """
    A parametric filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> mid_eq = supriya.ugens.MidEQ.ar(
        ...     db=0,
        ...     frequency=440,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> mid_eq
        <MidEQ.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, reciprocal_of_q: UGenRecursiveInput = 1.0, db: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, reciprocal_of_q: UGenRecursiveInput = 1.0, db: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class MoogFF(UGen):
    """
    A Moog VCF implementation.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> moog_ff = supriya.ugens.MoogFF.ar(
        ...     frequency=100,
        ...     gain=2,
        ...     reset=0,
        ...     source=source,
        ... )
        >>> moog_ff
        <MoogFF.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 100.0, gain: UGenRecursiveInput = 2.0, reset: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 100.0, gain: UGenRecursiveInput = 2.0, reset: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class MostChange(UGen):
    """
    Outputs most changed input.
    
    ::
    
        >>> most_change = supriya.ugens.MostChange.ar(
        ...     a=0,
        ...     b=0,
        ... )
        >>> most_change
        <MostChange.ar()[0]>
    """
    @classmethod
    def ar(cls, *, a: UGenRecursiveInput = 0, b: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, a: UGenRecursiveInput = 0, b: UGenRecursiveInput = 0) -> UGenOperable: ...
class MouseButton(UGen):
    """
    A mouse-button tracker.
    
    ::
    
        >>> supriya.ugens.MouseButton.kr()
        <MouseButton.kr()[0]>
    """
    @classmethod
    def kr(cls, *, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0, lag: UGenRecursiveInput = 0.2) -> UGenOperable: ...
class MouseX(UGen):
    """
    A mouse cursor tracker.
    
    MouseX tracks the y-axis of the mouse cursor position.
    
    ::
    
        >>> supriya.ugens.MouseX.kr()
        <MouseX.kr()[0]>
    """
    @classmethod
    def kr(cls, *, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0, warp: UGenRecursiveInput = 0.0, lag: UGenRecursiveInput = 0.2) -> UGenOperable: ...
class MouseY(UGen):
    """
    A mouse cursor tracker.
    
    MouseY tracks the y-axis of the mouse cursor position.
    
    ::
    
        >>> supriya.ugens.MouseY.kr()
        <MouseY.kr()[0]>
    """
    @classmethod
    def kr(cls, *, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0, warp: UGenRecursiveInput = 0.0, lag: UGenRecursiveInput = 0.2) -> UGenOperable: ...
class MulAdd(UGen):
    """
    An Optimized multiplication / addition ugen.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> mul_add = supriya.ugens.MulAdd.new(
        ...     addend=0.5,
        ...     multiplier=-1.5,
        ...     source=source,
        ... )
        >>> mul_add
        <MulAdd.ar()>
    """
    @classmethod
    def new(cls, *, source: UGenRecursiveInput, multiplier: UGenRecursiveInput = 1.0, addend: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class NRand(UGen):
    """
    A sum of `n` uniform distributions.
    
    ::
    
        >>> n_rand = supriya.ugens.NRand.ir(
        ...     minimum=-1,
        ...     maximum=1,
        ...     n=1,
        ... )
        >>> n_rand
        <NRand.ir()[0]>
    """
    @classmethod
    def ir(cls, *, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0, n: UGenRecursiveInput = 1) -> UGenOperable: ...
class NodeID(UGen):
    """
    A node ID info unit generator.
    
    ::
    
        >>> supriya.ugens.NodeID.ir()
        <NodeID.ir()[0]>
    """
    @classmethod
    def ir(cls) -> UGenOperable: ...
class Normalizer(UGen):
    """
    A dynamics flattener.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> normalizer = supriya.ugens.Normalizer.ar(
        ...     duration=0.01,
        ...     level=1,
        ...     source=source,
        ... )
        >>> normalizer
        <Normalizer.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, level: UGenRecursiveInput = 1.0, duration: UGenRecursiveInput = 0.01) -> UGenOperable: ...
class NumAudioBuses(UGen):
    """
    A number of audio buses info unit generator.
    
    ::
    
        >>> supriya.ugens.NumAudioBuses.ir()
        <NumAudioBuses.ir()[0]>
    """
    @classmethod
    def ir(cls) -> UGenOperable: ...
class NumBuffers(UGen):
    """
    A number of buffers info unit generator.
    
    ::
    
        >>> supriya.ugens.NumBuffers.ir()
        <NumBuffers.ir()[0]>
    """
    @classmethod
    def ir(cls) -> UGenOperable: ...
class NumControlBuses(UGen):
    """
    A number of control buses info unit generator.
    
    ::
    
        >>> supriya.ugens.NumControlBuses.ir()
        <NumControlBuses.ir()[0]>
    """
    @classmethod
    def ir(cls) -> UGenOperable: ...
class NumInputBuses(UGen):
    """
    A number of input buses info unit generator.
    
    ::
    
        >>> supriya.ugens.NumInputBuses.ir()
        <NumInputBuses.ir()[0]>
    """
    @classmethod
    def ir(cls) -> UGenOperable: ...
class NumOutputBuses(UGen):
    """
    A number of output buses info unit generator.
    
    ::
    
        >>> supriya.ugens.NumOutputBuses.ir()
        <NumOutputBuses.ir()[0]>
    """
    @classmethod
    def ir(cls) -> UGenOperable: ...
class NumRunningSynths(UGen):
    """
    A number of running synths info unit generator.
    
    ::
    
        >>> supriya.ugens.NumRunningSynths.ir()
        <NumRunningSynths.ir()[0]>
    """
    @classmethod
    def kr(cls) -> UGenOperable: ...
    @classmethod
    def ir(cls) -> UGenOperable: ...
class OffsetOut(UGen):
    """
    A bus output unit generator with sample-accurate timing.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.OffsetOut.ar(
        ...     bus=0,
        ...     source=source,
        ... )
        <OffsetOut.ar()>
    """
    @classmethod
    def ar(cls, *, bus: UGenRecursiveInput = 0, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, bus: UGenRecursiveInput = 0, source: UGenRecursiveInput) -> UGenOperable: ...
class OnePole(UGen):
    """
    A one pole filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> one_pole = supriya.ugens.OnePole.ar(
        ...     coefficient=0.5,
        ...     source=source,
        ... )
        >>> one_pole
        <OnePole.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, coefficient: UGenRecursiveInput = 0.5) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, coefficient: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class OneZero(UGen):
    """
    A one zero filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> one_zero = supriya.ugens.OneZero.ar(
        ...     coefficient=0.5,
        ...     source=source,
        ... )
        >>> one_zero
        <OneZero.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, coefficient: UGenRecursiveInput = 0.5) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, coefficient: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class Onsets(UGen):
    """
    An onset detector.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> onsets = supriya.ugens.Onsets.kr(
        ...     pv_chain=pv_chain,
        ...     floor_=0.1,
        ...     medianspan=11,
        ...     mingap=10,
        ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
        ...     rawodf=0,
        ...     relaxtime=1,
        ...     threshold=0.5,
        ...     whtype=1,
        ... )
        >>> onsets
        <Onsets.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, threshold: UGenRecursiveInput = 0.5, odftype: UGenRecursiveInput = 3, relaxtime: UGenRecursiveInput = 1, floor_: UGenRecursiveInput = 0.1, mingap: UGenRecursiveInput = 10, medianspan: UGenRecursiveInput = 11, whtype: UGenRecursiveInput = 1, rawodf: UGenRecursiveInput = 0) -> UGenOperable: ...
class Osc(UGen):
    """
    An interpolating wavetable oscillator.
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class OscN(UGen):
    """
    A non-interpolating wavetable oscillator.
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class Out(UGen):
    """
    A bus output unit generator.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.Out.ar(
        ...     bus=0,
        ...     source=source,
        ... )
        <Out.ar()>
    """
    @classmethod
    def ar(cls, *, bus: UGenRecursiveInput = 0, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, bus: UGenRecursiveInput = 0, source: UGenRecursiveInput) -> UGenOperable: ...
class PV_Add(UGen):
    """
    Complex addition.
    
    ::
    
        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_add = supriya.ugens.PV_Add.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_add
        <PV_Add.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain_a: UGenRecursiveInput, pv_chain_b: UGenRecursiveInput) -> UGenOperable: ...
class PV_BinScramble(UGen):
    """
    Scrambles bins.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_bin_scramble = supriya.ugens.PV_BinScramble.kr(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ...     width=0.2,
        ...     wipe=0,
        ... )
        >>> pv_bin_scramble
        <PV_BinScramble.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, wipe: UGenRecursiveInput = 0, width: UGenRecursiveInput = 0.2, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_BinShift(UGen):
    """
    Shifts and stretches bin positions.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_bin_shift = supriya.ugens.PV_BinShift.kr(
        ...     pv_chain=pv_chain,
        ...     interpolate=0,
        ...     shift=0,
        ...     stretch=1,
        ... )
        >>> pv_bin_shift
        <PV_BinShift.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, stretch: UGenRecursiveInput = 1.0, shift: UGenRecursiveInput = 0.0, interpolate: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_BinWipe(UGen):
    """
    Copies low bins from one input and the high bins of the other.
    
    ::
    
        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_bin_wipe = supriya.ugens.PV_BinWipe.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     wipe=0,
        ... )
        >>> pv_bin_wipe
        <PV_BinWipe.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain_a: UGenRecursiveInput, pv_chain_b: UGenRecursiveInput, wipe: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_BrickWall(UGen):
    """
    Zeros bins.
    
    - If wipe == 0 then there is no effect.
    - If wipe > 0 then it acts like a high pass filter, clearing bins from the bottom
      up.
    - If wipe < 0 then it acts like a low pass filter, clearing bins from the top down.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_brick_wall = supriya.ugens.PV_BrickWall.kr(
        ...     pv_chain=pv_chain,
        ...     wipe=0,
        ... )
        >>> pv_brick_wall
        <PV_BrickWall.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, wipe: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_ChainUGen(UGen):
    """
    Abstract base class for all phase-vocoder-chain unit generators.
    """
    ...
class PV_ConformalMap(UGen):
    """
    Complex plane attack.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_conformal_map = supriya.ugens.PV_ConformalMap.kr(
        ...     aimag=0,
        ...     areal=0,
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_conformal_map
        <PV_ConformalMap.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, areal: UGenRecursiveInput = 0, aimag: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_Conj(UGen):
    """
    Complex conjugate.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_conj = supriya.ugens.PV_Conj.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_conj
        <PV_Conj.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput) -> UGenOperable: ...
class PV_Copy(UGen):
    """
    Copies an FFT buffer.
    
    ::
    
        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_copy = supriya.ugens.PV_Copy.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_copy
        <PV_Copy.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain_a: UGenRecursiveInput, pv_chain_b: UGenRecursiveInput) -> UGenOperable: ...
class PV_CopyPhase(UGen):
    """
    Copies magnitudes and phases.
    
    ::
    
        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_copy_phase = supriya.ugens.PV_CopyPhase.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_copy_phase
        <PV_CopyPhase.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain_a: UGenRecursiveInput, pv_chain_b: UGenRecursiveInput) -> UGenOperable: ...
class PV_Diffuser(UGen):
    """
    Shifts phases randomly.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_diffuser = supriya.ugens.PV_Diffuser.kr(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ... )
        >>> pv_diffuser
        <PV_Diffuser.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_Div(UGen):
    """
    Complex division.
    
    ::
    
        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_div = supriya.ugens.PV_Div.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_div
        <PV_Div.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain_a: UGenRecursiveInput, pv_chain_b: UGenRecursiveInput) -> UGenOperable: ...
class PV_HainsworthFoote(UGen):
    """
    A FFT onset detector.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_hainsworth_foote = supriya.ugens.PV_HainsworthFoote.kr(
        ...     pv_chain=pv_chain,
        ...     propf=0,
        ...     proph=0,
        ...     threshold=1,
        ...     waittime=0.04,
        ... )
        >>> pv_hainsworth_foote
        <PV_HainsworthFoote.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, proph: UGenRecursiveInput = 0, propf: UGenRecursiveInput = 0, threshold: UGenRecursiveInput = 1, waittime: UGenRecursiveInput = 0.04) -> UGenOperable: ...
class PV_JensenAndersen(UGen):
    """
    A FFT feature detector for onset detection.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_jensen_andersen = supriya.ugens.PV_JensenAndersen.kr(
        ...     pv_chain=pv_chain,
        ...     prophfc=0.25,
        ...     prophfe=0.25,
        ...     propsc=0.25,
        ...     propsf=0.25,
        ...     threshold=1,
        ...     waittime=0.04,
        ... )
        >>> pv_jensen_andersen
        <PV_JensenAndersen.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, propsc: UGenRecursiveInput = 0.25, prophfe: UGenRecursiveInput = 0.25, prophfc: UGenRecursiveInput = 0.25, propsf: UGenRecursiveInput = 0.25, threshold: UGenRecursiveInput = 1, waittime: UGenRecursiveInput = 0.04) -> UGenOperable: ...
class PV_LocalMax(UGen):
    """
    Passes bins which are local maxima.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_local_max = supriya.ugens.PV_LocalMax.kr(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ... )
        >>> pv_local_max
        <PV_LocalMax.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, threshold: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_MagAbove(UGen):
    """
    Passes magnitudes above threshold.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_above = supriya.ugens.PV_MagAbove.kr(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ... )
        >>> pv_mag_above
        <PV_MagAbove.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, threshold: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_MagBelow(UGen):
    """
    Passes magnitudes below threshold.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_below = supriya.ugens.PV_MagBelow.kr(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ... )
        >>> pv_mag_below
        <PV_MagBelow.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, threshold: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_MagClip(UGen):
    """
    Clips magnitudes.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_clip = supriya.ugens.PV_MagClip.kr(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ... )
        >>> pv_mag_clip
        <PV_MagClip.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, threshold: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_MagDiv(UGen):
    """
    Divides magnitudes.
    
    ::
    
        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_mag_div = supriya.ugens.PV_MagDiv.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     zeroed=0.0001,
        ... )
        >>> pv_mag_div
        <PV_MagDiv.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain_a: UGenRecursiveInput, pv_chain_b: UGenRecursiveInput, zeroed: UGenRecursiveInput = 0.0001) -> UGenOperable: ...
class PV_MagFreeze(UGen):
    """
    Freezes magnitudes.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_freeze = supriya.ugens.PV_MagFreeze.kr(
        ...     pv_chain=pv_chain,
        ...     freeze=0,
        ... )
        >>> pv_mag_freeze
        <PV_MagFreeze.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, freeze: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_MagMul(UGen):
    """
    Multiplies FFT magnitudes.
    
    ::
    
        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_mag_mul = supriya.ugens.PV_MagMul.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_mag_mul
        <PV_MagMul.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain_a: UGenRecursiveInput, pv_chain_b: UGenRecursiveInput) -> UGenOperable: ...
class PV_MagNoise(UGen):
    """
    Multiplies magnitudes by noise.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_noise = supriya.ugens.PV_MagNoise.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_mag_noise
        <PV_MagNoise.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput) -> UGenOperable: ...
class PV_MagShift(UGen):
    """
    Shifts and stretches magnitude bin position.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_shift = supriya.ugens.PV_MagShift.kr(
        ...     pv_chain=pv_chain,
        ...     shift=0,
        ...     stretch=1,
        ... )
        >>> pv_mag_shift
        <PV_MagShift.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, stretch: UGenRecursiveInput = 1.0, shift: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class PV_MagSmear(UGen):
    """
    Averages magnitudes across bins.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_smear = supriya.ugens.PV_MagSmear.kr(
        ...     bins=0,
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_mag_smear
        <PV_MagSmear.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, bins: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_MagSquared(UGen):
    """
    Squares magnitudes.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_mag_squared = supriya.ugens.PV_MagSquared.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_mag_squared
        <PV_MagSquared.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput) -> UGenOperable: ...
class PV_Max(UGen):
    """
    Maximum magnitude.
    
    ::
    
        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_max = supriya.ugens.PV_Max.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_max
        <PV_Max.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain_a: UGenRecursiveInput, pv_chain_b: UGenRecursiveInput) -> UGenOperable: ...
class PV_Min(UGen):
    """
    Minimum magnitude.
    
    ::
    
        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_min = supriya.ugens.PV_Min.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_min
        <PV_Min.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain_a: UGenRecursiveInput, pv_chain_b: UGenRecursiveInput) -> UGenOperable: ...
class PV_Mul(UGen):
    """
    Complex multiplication.
    
    ::
    
        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_mul = supriya.ugens.PV_Mul.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ... )
        >>> pv_mul
        <PV_Mul.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain_a: UGenRecursiveInput, pv_chain_b: UGenRecursiveInput) -> UGenOperable: ...
class PV_PhaseShift(UGen):
    """
    Shifts phase.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> shift = supriya.ugens.LFNoise2.kr(frequency=1).scale(-1, 1, -180, 180)
        >>> pv_phase_shift = supriya.ugens.PV_PhaseShift.kr(
        ...     pv_chain=pv_chain,
        ...     integrate=0,
        ...     shift=shift,
        ... )
        >>> pv_phase_shift
        <PV_PhaseShift.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, shift: UGenRecursiveInput, integrate: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_PhaseShift270(UGen):
    """
    Shifts phase by 270 degrees.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_phase_shift_270 = supriya.ugens.PV_PhaseShift270.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_phase_shift_270
        <PV_PhaseShift270.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput) -> UGenOperable: ...
class PV_PhaseShift90(UGen):
    """
    Shifts phase by 90 degrees.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_phase_shift_90 = supriya.ugens.PV_PhaseShift90.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> pv_phase_shift_90
        <PV_PhaseShift90.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput) -> UGenOperable: ...
class PV_RandComb(UGen):
    """
    Passes random bins.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_rand_comb = supriya.ugens.PV_RandComb.kr(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ...     wipe=0,
        ... )
        >>> pv_rand_comb
        <PV_RandComb.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, wipe: UGenRecursiveInput = 0, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_RandWipe(UGen):
    """
    Crossfades in random bin order.
    
    ::
    
        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_rand_wipe = supriya.ugens.PV_RandWipe.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     trigger=0,
        ...     wipe=0,
        ... )
        >>> pv_rand_wipe
        <PV_RandWipe.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain_a: UGenRecursiveInput, pv_chain_b: UGenRecursiveInput, wipe: UGenRecursiveInput = 0, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
class PV_RectComb(UGen):
    """
    Makes gaps in the spectrum.
    
    ::
    
        >>> pv_chain = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_rect_comb = supriya.ugens.PV_RectComb.kr(
        ...     pv_chain=pv_chain,
        ...     num_teeth=0,
        ...     phase=0,
        ...     width=0.5,
        ... )
        >>> pv_rect_comb
        <PV_RectComb.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, num_teeth: UGenRecursiveInput = 0, phase: UGenRecursiveInput = 0, width: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class PV_RectComb2(UGen):
    """
    Makes gaps in the spectrum.
    
    ::
    
        >>> pv_chain_a = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ... )
        >>> pv_chain_b = supriya.ugens.FFT.kr(
        ...     source=supriya.ugens.LFSaw.ar(),
        ... )
        >>> pv_rect_comb_2 = supriya.ugens.PV_RectComb2.kr(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     num_teeth=0,
        ...     phase=0,
        ...     width=0.5,
        ... )
        >>> pv_rect_comb_2
        <PV_RectComb2.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain_a: UGenRecursiveInput, pv_chain_b: UGenRecursiveInput, num_teeth: UGenRecursiveInput = 0, phase: UGenRecursiveInput = 0, width: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class Pan2(UGen):
    """
    A two channel equal power panner.
    
    ::
    
        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> pan_2 = supriya.ugens.Pan2.ar(
        ...     source=source,
        ... )
        >>> pan_2
        <Pan2.ar()>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, position: UGenRecursiveInput = 0.0, level: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, position: UGenRecursiveInput = 0.0, level: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class Pan4(UGen):
    """
    A four-channel equal-power panner.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pan_4 = supriya.ugens.Pan4.ar(
        ...     gain=1,
        ...     source=source,
        ...     x_position=0,
        ...     y_position=0,
        ... )
        >>> pan_4
        <Pan4.ar()>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, x_position: UGenRecursiveInput = 0, y_position: UGenRecursiveInput = 0, gain: UGenRecursiveInput = 1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, x_position: UGenRecursiveInput = 0, y_position: UGenRecursiveInput = 0, gain: UGenRecursiveInput = 1) -> UGenOperable: ...
class PanAz(UGen):
    """
    A multi-channel equal-power panner.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pan_az = supriya.ugens.PanAz.ar(
        ...     channel_count=8,
        ...     amplitude=1,
        ...     orientation=0.5,
        ...     position=0,
        ...     source=source,
        ...     width=2,
        ... )
        >>> pan_az
        <PanAz.ar()>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, position: UGenRecursiveInput = 0, amplitude: UGenRecursiveInput = 1, width: UGenRecursiveInput = 2, orientation: UGenRecursiveInput = 0.5, channel_count: int = 1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, position: UGenRecursiveInput = 0, amplitude: UGenRecursiveInput = 1, width: UGenRecursiveInput = 2, orientation: UGenRecursiveInput = 0.5, channel_count: int = 1) -> UGenOperable: ...
class PanB(UGen):
    """
    A 3D ambisonic b-format panner.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pan_b = supriya.ugens.PanB.ar(
        ...     azimuth=0,
        ...     elevation=0,
        ...     gain=1,
        ...     source=source,
        ... )
        >>> pan_b
        <PanB.ar()>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, azimuth: UGenRecursiveInput = 0, elevation: UGenRecursiveInput = 0, gain: UGenRecursiveInput = 1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, azimuth: UGenRecursiveInput = 0, elevation: UGenRecursiveInput = 0, gain: UGenRecursiveInput = 1) -> UGenOperable: ...
class PanB2(UGen):
    """
    A 2D ambisonic b-format panner.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pan_b_2 = supriya.ugens.PanB2.ar(
        ...     azimuth=0,
        ...     gain=1,
        ...     source=source,
        ... )
        >>> pan_b_2
        <PanB2.ar()>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, azimuth: UGenRecursiveInput = 0, gain: UGenRecursiveInput = 1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, azimuth: UGenRecursiveInput = 0, gain: UGenRecursiveInput = 1) -> UGenOperable: ...
class Parameter(UGen):
    """
    A UGen: a "unit generator".
    """
    ...
class Pause(UGen):
    """
    Pauses the node at `node_id` when triggered by `trigger`.
    
    ::
    
        >>> node_id = 1000
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> pause = supriya.ugens.Pause.kr(
        ...     node_id=node_id,
        ...     trigger=trigger,
        ... )
        >>> pause
        <Pause.kr()[0]>
    """
    @classmethod
    def kr(cls, *, trigger: UGenRecursiveInput, node_id: UGenRecursiveInput) -> UGenOperable: ...
class PauseSelf(UGen):
    """
    Pauses the enclosing synth when triggered by `trigger`.
    
    ::
    
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> pause_self = supriya.ugens.PauseSelf.kr(
        ...     trigger=trigger,
        ... )
        >>> pause_self
        <PauseSelf.kr()[0]>
    """
    @classmethod
    def kr(cls, *, trigger: UGenRecursiveInput) -> UGenOperable: ...
class PauseSelfWhenDone(UGen):
    """
    Pauses the enclosing synth when `source` sets its `done` flag.
    
    ::
    
        >>> source = supriya.ugens.Line.kr()
        >>> pause_self_when_done = supriya.ugens.PauseSelfWhenDone.kr(
        ...     source=source,
        ... )
        >>> pause_self_when_done
        <PauseSelfWhenDone.kr()[0]>
    """
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class Peak(UGen):
    """
    Tracks peak signal amplitude.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
        >>> peak = supriya.ugens.Peak.ar(
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> peak
        <Peak.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
class PeakFollower(UGen):
    """
    Tracks peak signal amplitude.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> peak_follower = supriya.ugens.PeakFollower.ar(
        ...     decay=0.999,
        ...     source=source,
        ... )
        >>> peak_follower
        <PeakFollower.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, decay: UGenRecursiveInput = 0.999) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, decay: UGenRecursiveInput = 0.999) -> UGenOperable: ...
class Phasor(UGen):
    """
    A resettable linear ramp between two levels.
    
    ::
    
        >>> trigger = supriya.ugens.Impulse.kr(frequency=0.5)
        >>> phasor = supriya.ugens.Phasor.ar(
        ...     rate=1,
        ...     reset_pos=0,
        ...     start=0,
        ...     stop=1,
        ...     trigger=trigger,
        ... )
        >>> phasor
        <Phasor.ar()[0]>
    """
    @classmethod
    def ar(cls, *, trigger: UGenRecursiveInput = 0, rate: UGenRecursiveInput = 1.0, start: UGenRecursiveInput = 0.0, stop: UGenRecursiveInput = 1.0, reset_pos: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, trigger: UGenRecursiveInput = 0, rate: UGenRecursiveInput = 1.0, start: UGenRecursiveInput = 0.0, stop: UGenRecursiveInput = 1.0, reset_pos: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class PinkNoise(UGen):
    """
    A pink noise unit generator.
    
    ::
    
        >>> supriya.ugens.PinkNoise.ar()
        <PinkNoise.ar()[0]>
    """
    @classmethod
    def ar(cls) -> UGenOperable: ...
    @classmethod
    def kr(cls) -> UGenOperable: ...
class Pitch(UGen):
    """
    An autocorrelation pitch follower.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pitch = supriya.ugens.Pitch.kr(source=source)
        >>> pitch
        <Pitch.kr()>
    """
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, initial_frequency: UGenRecursiveInput = 440, min_frequency: UGenRecursiveInput = 60, max_frequency: UGenRecursiveInput = 4000, exec_frequency: UGenRecursiveInput = 100, max_bins_per_octave: UGenRecursiveInput = 16, median: UGenRecursiveInput = 1, amplitude_threshold: UGenRecursiveInput = 0.01, peak_threshold: UGenRecursiveInput = 0.5, down_sample_factor: UGenRecursiveInput = 1, clarity: UGenRecursiveInput = 0) -> UGenOperable: ...
class PitchShift(UGen):
    """
    A pitch shift unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.PitchShift.ar(
        ...     source=source,
        ... )
        <PitchShift.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, window_size: UGenRecursiveInput = 0.2, pitch_ratio: UGenRecursiveInput = 1.0, pitch_dispersion: UGenRecursiveInput = 0.0, time_dispersion: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class PlayBuf(UGen):
    """
    A sample playback oscillator.
    
    ::
    
        >>> buffer_id = 23
        >>> play_buf = supriya.ugens.PlayBuf.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     done_action=0,
        ...     loop=0,
        ...     rate=1,
        ...     start_position=0,
        ...     trigger=1,
        ... )
        >>> play_buf
        <PlayBuf.ar()>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, rate: UGenRecursiveInput = 1, trigger: UGenRecursiveInput = 1, start_position: UGenRecursiveInput = 0, loop: UGenRecursiveInput = 0, done_action: UGenRecursiveInput = 0, channel_count: int = 1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, rate: UGenRecursiveInput = 1, trigger: UGenRecursiveInput = 1, start_position: UGenRecursiveInput = 0, loop: UGenRecursiveInput = 0, done_action: UGenRecursiveInput = 0, channel_count: int = 1) -> UGenOperable: ...
class Pluck(UGen):
    """
    A Karplus-String UGen.
    
    ::
    
        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(density=2)
        >>> pluck = supriya.ugens.Pluck.ar(
        ...     coefficient=0.5,
        ...     decay_time=1,
        ...     delay_time=0.2,
        ...     maximum_delay_time=0.2,
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> pluck
        <Pluck.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, trigger: UGenRecursiveInput, maximum_delay_time: UGenRecursiveInput = 0.2, delay_time: UGenRecursiveInput = 0.2, decay_time: UGenRecursiveInput = 1, coefficient: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class Poll(UGen):
    """
    A UGen poller.
    
    ::
    
        >>> sine = supriya.ugens.SinOsc.ar()
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
        >>> poll = supriya.ugens.Poll.ar(
        ...     source=sine,
        ...     trigger=trigger,
        ...     trigger_id=1234,
        ... )
        >>> poll
        <Poll.ar()[0]>
    
    .. container:: example
    
        Unlike **sclang**, Python does not share any inter-process communication with
        **scsynth**. This means that the Poll UGen is not able to automatically print
        out its diagnostic messages into a Python interpreter session.
    
        To get information out of the Poll UGen, we first need to set the Poll's
        `trigger_id` to a value greater than 0. This will cause the poll to send `/tr`
        OSC messages back to its client - Python. We can then register a callback to
        respond to these `/tr` messages.
    
        ::
    
            >>> with supriya.SynthDefBuilder() as builder:
            ...     sine = supriya.ugens.SinOsc.ar()
            ...     trigger = supriya.ugens.Impulse.kr(frequency=1)
            ...     poll = supriya.ugens.Poll.ar(
            ...         source=sine,
            ...         trigger=trigger,
            ...         trigger_id=1234,
            ...     )
            ...
            >>> synthdef = builder.build()
    
        ::
    
            >>> server = supriya.Server().boot(port=supriya.osc.find_free_port())
            >>> _ = server.add_synthdefs(
            ...     synthdef,
            ...     on_completion=lambda context: context.add_synth(synthdef),
            ... )
            >>> _ = server.sync()
            >>> callback = server.osc_protocol.register(
            ...     pattern="/tr",
            ...     procedure=lambda message: print(
            ...         "Polled: {!r}".format(message)
            ...     ),
            ...     once=True,
            ... )
    
        ::
    
            >>> _ = server.quit()
    """
    @classmethod
    def ar(cls, label: UGenRecursiveInput = None, source: UGenRecursiveInput = None, trigger: UGenRecursiveInput = None, trigger_id: UGenRecursiveInput = -1) -> UGenOperable: ...
    @classmethod
    def kr(cls, label: UGenRecursiveInput = None, source: UGenRecursiveInput = None, trigger: UGenRecursiveInput = None, trigger_id: UGenRecursiveInput = -1) -> UGenOperable: ...
    @classmethod
    def new(cls, label: UGenRecursiveInput = None, source: UGenRecursiveInput = None, trigger: UGenRecursiveInput = None, trigger_id: UGenRecursiveInput = -1) -> UGenOperable: ...
class Pulse(UGen):
    """
    Band limited pulse wave generator with pulse width modulation.
    
    ::
    
        >>> pulse = supriya.ugens.Pulse.ar(
        ...     frequency=440,
        ...     width=0.5,
        ... )
        >>> pulse
        <Pulse.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 440.0, width: UGenRecursiveInput = 0.5) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 440.0, width: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class QuadC(UGen):
    """
    A cubic-interpolating general quadratic map chaotic generator.
    
    ::
    
        >>> quad_c = supriya.ugens.QuadC.ar(
        ...     a=1,
        ...     b=-1,
        ...     c=-0.75,
        ...     frequency=22050,
        ...     xi=0,
        ... )
        >>> quad_c
        <QuadC.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1, b: UGenRecursiveInput = -1, c: UGenRecursiveInput = -0.75, xi: UGenRecursiveInput = 0) -> UGenOperable: ...
class QuadL(UGen):
    """
    A linear-interpolating general quadratic map chaotic generator.
    
    ::
    
        >>> quad_l = supriya.ugens.QuadL.ar(
        ...     a=1,
        ...     b=-1,
        ...     c=-0.75,
        ...     frequency=22050,
        ...     xi=0,
        ... )
        >>> quad_l
        <QuadL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1, b: UGenRecursiveInput = -1, c: UGenRecursiveInput = -0.75, xi: UGenRecursiveInput = 0) -> UGenOperable: ...
class QuadN(UGen):
    """
    A non-interpolating general quadratic map chaotic generator.
    
    ::
    
        >>> quad_n = supriya.ugens.QuadN.ar(
        ...     a=1,
        ...     b=-1,
        ...     c=-0.75,
        ...     frequency=22050,
        ...     xi=0,
        ... )
        >>> quad_n
        <QuadN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, a: UGenRecursiveInput = 1, b: UGenRecursiveInput = -1, c: UGenRecursiveInput = -0.75, xi: UGenRecursiveInput = 0) -> UGenOperable: ...
class RHPF(UGen):
    """
    A resonant highpass filter unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.RLPF.ar(source=source)
        <RLPF.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, reciprocal_of_q: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, reciprocal_of_q: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class RLPF(UGen):
    """
    A resonant lowpass filter unit generator.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.RLPF.ar(source=source)
        <RLPF.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, reciprocal_of_q: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, reciprocal_of_q: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class RadiansPerSample(UGen):
    """
    A radians-per-sample info unit generator.
    
    ::
    
        >>> supriya.ugens.RadiansPerSample.ir()
        <RadiansPerSample.ir()[0]>
    """
    @classmethod
    def ir(cls) -> UGenOperable: ...
class Ramp(UGen):
    """
    Breaks a continuous signal into line segments.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> ramp = supriya.ugens.Ramp.ar(
        ...     lag_time=0.1,
        ...     source=source,
        ... )
        >>> ramp
        <Ramp.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, lag_time: UGenRecursiveInput = 0.1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, lag_time: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class Rand(UGen):
    """
    A uniform random distribution.
    
    ::
    
        >>> supriya.ugens.Rand.ir()
        <Rand.ir()[0]>
    """
    @classmethod
    def ir(cls, *, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class RandID(UGen):
    """
    Sets the synth's random generator ID.
    
    ::
    
        >>> rand_id = supriya.ugens.RandID.ir(
        ...     rand_id=1,
        ... )
        >>> rand_id
        <RandID.ir()[0]>
    """
    @classmethod
    def kr(cls, *, rand_id: UGenRecursiveInput = 1) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, rand_id: UGenRecursiveInput = 1) -> UGenOperable: ...
class RandSeed(UGen):
    """
    Sets the synth's random generator seed.
    
    ::
    
        >>> trigger = supriya.ugens.Impulse.ar()
        >>> rand_seed = supriya.ugens.RandSeed.ar(
        ...     seed=1,
        ...     trigger=trigger,
        ... )
        >>> rand_seed
        <RandSeed.ar()[0]>
    """
    @classmethod
    def ar(cls, *, trigger: UGenRecursiveInput = 0, seed: UGenRecursiveInput = 56789) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, trigger: UGenRecursiveInput = 0, seed: UGenRecursiveInput = 56789) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, trigger: UGenRecursiveInput = 0, seed: UGenRecursiveInput = 56789) -> UGenOperable: ...
class RecordBuf(UGen):
    """
    Records or overdubs into a buffer.
    
    ::
    
        >>> buffer_id = 23
        >>> source = supriya.ugens.In.ar(bus=0, channel_count=2)
        >>> record_buf = supriya.ugens.RecordBuf.ar(
        ...     buffer_id=buffer_id,
        ...     done_action=0,
        ...     loop=1,
        ...     offset=0,
        ...     preexisting_level=0,
        ...     record_level=1,
        ...     run=1,
        ...     source=source,
        ...     trigger=1,
        ... )
        >>> record_buf
        <RecordBuf.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, offset: UGenRecursiveInput = 0.0, record_level: UGenRecursiveInput = 1.0, preexisting_level: UGenRecursiveInput = 0.0, run: UGenRecursiveInput = 1.0, loop: UGenRecursiveInput = 1.0, trigger: UGenRecursiveInput = 1.0, done_action: UGenRecursiveInput = DoneAction.NOTHING, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, offset: UGenRecursiveInput = 0.0, record_level: UGenRecursiveInput = 1.0, preexisting_level: UGenRecursiveInput = 0.0, run: UGenRecursiveInput = 1.0, loop: UGenRecursiveInput = 1.0, trigger: UGenRecursiveInput = 1.0, done_action: UGenRecursiveInput = DoneAction.NOTHING, source: UGenRecursiveInput) -> UGenOperable: ...
class ReplaceOut(UGen):
    """
    An overwriting bus output unit generator.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.ReplaceOut.ar(
        ...     bus=0,
        ...     source=source,
        ... )
        <ReplaceOut.ar()>
    """
    @classmethod
    def ar(cls, *, bus: UGenRecursiveInput = 0, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, bus: UGenRecursiveInput = 0, source: UGenRecursiveInput) -> UGenOperable: ...
class Ringz(UGen):
    """
    A ringing filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> ringz = supriya.ugens.Ringz.ar(
        ...     decay_time=1,
        ...     frequency=440,
        ...     source=source,
        ... )
        >>> ringz
        <Ringz.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, decay_time: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class Rotate2(UGen):
    """
    Equal-power sound-field rotator.
    
    ::
    
        >>> x = supriya.ugens.PinkNoise.ar() * 0.4
        >>> y = supriya.ugens.LFTri.ar(frequency=880)
        >>> y *= supriya.ugens.LFPulse.kr(frequency=3, width=0.1)
        >>> position = supriya.ugens.LFSaw.kr(frequency=0.1)
        >>> rotate_2 = supriya.ugens.Rotate2.ar(
        ...     x=x,
        ...     y=y,
        ...     position=position,
        ... )
        >>> rotate_2
        <Rotate2.ar()>
    
    Returns an array of the rotator's left and right outputs.
    """
    @classmethod
    def ar(cls, *, x: UGenRecursiveInput, y: UGenRecursiveInput, position: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, x: UGenRecursiveInput, y: UGenRecursiveInput, position: UGenRecursiveInput = 0) -> UGenOperable: ...
class RunningMax(UGen):
    """
    Tracks maximum signal amplitude.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
        >>> running_max = supriya.ugens.RunningMax.ar(
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> running_max
        <RunningMax.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
class RunningMin(UGen):
    """
    Tracks minimum signal amplitude.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
        >>> running_min = supriya.ugens.RunningMin.ar(
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> running_min
        <RunningMin.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
class RunningSum(UGen):
    """
    Tracks running sum over ``n`` frames.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> running_sum = supriya.ugens.RunningSum.ar(
        ...     sample_count=40,
        ...     source=source,
        ... )
        >>> running_sum
        <RunningSum.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, sample_count: UGenRecursiveInput = 40) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, sample_count: UGenRecursiveInput = 40) -> UGenOperable: ...
class SOS(UGen):
    """
    A second-order filter section.
    
    ::
    
        out(i) = (a0 * in(i)) + (a1 * in(i-1)) + (b1 * out(i-1))
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> sos = supriya.ugens.SOS.ar(
        ...     a_0=0,
        ...     a_1=0,
        ...     a_2=0,
        ...     b_1=0,
        ...     b_2=0,
        ...     source=source,
        ... )
        >>> sos
        <SOS.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, a_0: UGenRecursiveInput = 0.0, a_1: UGenRecursiveInput = 0.0, a_2: UGenRecursiveInput = 0.0, b_1: UGenRecursiveInput = 0.0, b_2: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, a_0: UGenRecursiveInput = 0.0, a_1: UGenRecursiveInput = 0.0, a_2: UGenRecursiveInput = 0.0, b_1: UGenRecursiveInput = 0.0, b_2: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class SampleDur(UGen):
    """
    A sample duration info unit generator.
    
    ::
    
        >>> supriya.ugens.SampleDur.ir()
        <SampleDur.ir()[0]>
    """
    @classmethod
    def ir(cls) -> UGenOperable: ...
class SampleRate(UGen):
    """
    A sample-rate info unit generator.
    
    ::
    
        >>> supriya.ugens.SampleRate.ir()
        <SampleRate.ir()[0]>
    """
    @classmethod
    def ir(cls) -> UGenOperable: ...
class Sanitize(UGen):
    """
    Remove infinity, NaN, and denormals.
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, replace: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, replace: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class Saw(UGen):
    """
    A band-limited sawtooth oscillator unit generator.
    
    ::
    
        >>> supriya.ugens.Saw.ar()
        <Saw.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 440.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 440.0) -> UGenOperable: ...
class Schmidt(UGen):
    """
    A Schmidt trigger.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> schmidt = supriya.ugens.Schmidt.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ... )
        >>> schmidt
        <Schmidt.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class ScopeOut(UGen):
    """
    Utility UGen for scope output on remote servers.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0, channel_count=2)
        >>> scope_out = supriya.ugens.ScopeOut.ar(
        ...     source=source,
        ...     buffer_id=0,
        ... )
        >>> scope_out
        <ScopeOut.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput) -> UGenOperable: ...
class ScopeOut2(UGen):
    """
    Utility UGen for scope output on local servers.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0, channel_count=2)
        >>> scope_out_2 = supriya.ugens.ScopeOut2.ar(
        ...     source=source,
        ...     scope_id=0,
        ...     max_frames=8192,
        ...     scope_frames=2048,
        ... )
        >>> scope_out_2
        <ScopeOut2.ar()[0]>
    """
    @classmethod
    def ar(cls, *, scope_id: UGenRecursiveInput, max_frames: UGenRecursiveInput = 4096, scope_frames: UGenRecursiveInput = Default(), source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, scope_id: UGenRecursiveInput, max_frames: UGenRecursiveInput = 4096, scope_frames: UGenRecursiveInput = Default(), source: UGenRecursiveInput) -> UGenOperable: ...
class Select(UGen):
    """
    A signal selector.
    
    ::
    
        >>> sources = supriya.ugens.In.ar(bus=0, channel_count=8)
        >>> selector = supriya.ugens.Phasor.kr() * 8
        >>> select = supriya.ugens.Select.ar(
        ...     sources=sources,
        ...     selector=selector,
        ... )
        >>> select
        <Select.ar()[0]>
    """
    @classmethod
    def ar(cls, *, selector: UGenRecursiveInput, sources: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, selector: UGenRecursiveInput, sources: UGenRecursiveInput) -> UGenOperable: ...
class SendPeakRMS(UGen):
    """
    Tracks peak and power of a signal for GUI applications.
    
    ::
    
        >>> send_peak_rms = supriya.ugens.SendPeakRMS.kr(
        ...     command_name="/reply",
        ...     peak_lag=3,
        ...     reply_id=-1,
        ...     reply_rate=20,
        ...     source=[1, 2, 3],
        ... )
        >>> send_peak_rms
        <SendPeakRMS.kr()>
    """
    @classmethod
    def ar(cls, command_name: UGenRecursiveInput = '/reply', peak_lag: UGenRecursiveInput = 3, reply_id: UGenRecursiveInput = -1, reply_rate: UGenRecursiveInput = 20, source: UGenRecursiveInput = None) -> UGenOperable: ...
    @classmethod
    def kr(cls, command_name: UGenRecursiveInput = '/reply', peak_lag: UGenRecursiveInput = 3, reply_id: UGenRecursiveInput = -1, reply_rate: UGenRecursiveInput = 20, source: UGenRecursiveInput = None) -> UGenOperable: ...
class SendReply(UGen):
    """
    Sends an array of values from the server to all notified clients.
    
    ::
    
        >>> source = supriya.ugens.In.ar(channel_count=4)
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
        >>> send_reply = supriya.ugens.SendReply.kr(
        ...     command_name="/reply",
        ...     source=source,
        ...     trigger=trigger,
        ... )
    """
    @classmethod
    def ar(cls, command_name: UGenRecursiveInput = '/reply', reply_id: UGenRecursiveInput = -1, source: UGenRecursiveInput = None, trigger: UGenRecursiveInput = None) -> UGenOperable: ...
    @classmethod
    def kr(cls, command_name: UGenRecursiveInput = '/reply', reply_id: UGenRecursiveInput = -1, source: UGenRecursiveInput = None, trigger: UGenRecursiveInput = None) -> UGenOperable: ...
class SendTrig(UGen):
    """
    A UGen: a "unit generator".
    """
    @classmethod
    def ar(cls, *, trigger: UGenRecursiveInput, id_: UGenRecursiveInput = 0, value: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, trigger: UGenRecursiveInput, id_: UGenRecursiveInput = 0, value: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class SinOsc(UGen):
    """
    A sinusoid oscillator unit generator.
    
    ::
    
        >>> supriya.ugens.SinOsc.ar()
        <SinOsc.ar()[0]>
    
    ::
    
        >>> print(_)
        synthdef:
            name: ...
            ugens:
            -   SinOsc.ar:
                    frequency: 440.0
                    phase: 0.0
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 440.0, phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 440.0, phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class Slew(UGen):
    """
    A slew rate limiter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> slew = supriya.ugens.Slew.ar(
        ...     source=source,
        ...     up=1,
        ...     down=1,
        ... )
        >>> slew
        <Slew.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, up: UGenRecursiveInput = 1.0, down: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, up: UGenRecursiveInput = 1.0, down: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class Slope(UGen):
    """
    Calculates slope of signal.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> slope = supriya.ugens.Slope.ar(
        ...     source=source,
        ... )
        >>> slope
        <Slope.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
class SpecCentroid(UGen):
    """
    A spectral centroid measure.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> spec_centroid = supriya.ugens.SpecCentroid.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> spec_centroid
        <SpecCentroid.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput) -> UGenOperable: ...
class SpecFlatness(UGen):
    """
    A spectral flatness measure.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> spec_flatness = supriya.ugens.SpecFlatness.kr(
        ...     pv_chain=pv_chain,
        ... )
        >>> spec_flatness
        <SpecFlatness.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput) -> UGenOperable: ...
class SpecPcile(UGen):
    """
    Find a percentile of FFT magnitude spectrum.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT.kr(source=source)
        >>> spec_pcile = supriya.ugens.SpecPcile.kr(
        ...     pv_chain=pv_chain,
        ...     fraction=0.5,
        ...     interpolate=0,
        ... )
        >>> spec_pcile
        <SpecPcile.kr()[0]>
    """
    @classmethod
    def kr(cls, *, pv_chain: UGenRecursiveInput, fraction: UGenRecursiveInput = 0.5, interpolate: UGenRecursiveInput = 0) -> UGenOperable: ...
class Spring(UGen):
    """
    A resonating spring physical model.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> spring = supriya.ugens.Spring.ar(
        ...     damping=0,
        ...     source=source,
        ...     spring=1,
        ... )
        >>> spring
        <Spring.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, spring: UGenRecursiveInput = 1.0, damping: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, spring: UGenRecursiveInput = 1.0, damping: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class StandardL(UGen):
    """
    A linear-interpolating standard map chaotic generator.
    
    ::
    
        >>> standard_l = supriya.ugens.StandardL.ar(
        ...     frequency=22050,
        ...     k=1,
        ...     xi=0.5,
        ...     yi=0,
        ... )
        >>> standard_l
        <StandardL.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, k: UGenRecursiveInput = 1, xi: UGenRecursiveInput = 0.5, yi: UGenRecursiveInput = 0) -> UGenOperable: ...
class StandardN(UGen):
    """
    A non-interpolating standard map chaotic generator.
    
    ::
    
        >>> standard_n = supriya.ugens.StandardN.ar(
        ...     frequency=22050,
        ...     k=1,
        ...     xi=0.5,
        ...     yi=0,
        ... )
        >>> standard_n
        <StandardN.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 22050, k: UGenRecursiveInput = 1, xi: UGenRecursiveInput = 0.5, yi: UGenRecursiveInput = 0) -> UGenOperable: ...
class SubsampleOffset(UGen):
    """
    A subsample-offset info unit generator.
    
    ::
    
        >>> supriya.ugens.SubsampleOffset.ir()
        <SubsampleOffset.ir()[0]>
    """
    @classmethod
    def ir(cls) -> UGenOperable: ...
class Sum3(UGen):
    """
    A three-input summing unit generator.
    
    ::
    
        >>> input_one = supriya.ugens.SinOsc.ar()
        >>> input_two = supriya.ugens.SinOsc.ar(phase=0.1)
        >>> input_three = supriya.ugens.SinOsc.ar(phase=0.2)
        >>> supriya.ugens.Sum3.new(
        ...     input_one=input_one,
        ...     input_two=input_two,
        ...     input_three=input_three,
        ... )
        <Sum3.ar()>
    """
    @classmethod
    def new(cls, *, input_one: UGenRecursiveInput, input_two: UGenRecursiveInput, input_three: UGenRecursiveInput) -> UGenOperable: ...
class Sum4(UGen):
    """
    A four-input summing unit generator.
    
    ::
    
        >>> input_one = supriya.ugens.SinOsc.ar()
        >>> input_two = supriya.ugens.SinOsc.ar(phase=0.1)
        >>> input_three = supriya.ugens.SinOsc.ar(phase=0.2)
        >>> input_four = supriya.ugens.SinOsc.ar(phase=0.3)
        >>> supriya.ugens.Sum4.new(
        ...     input_one=input_one,
        ...     input_two=input_two,
        ...     input_three=input_three,
        ...     input_four=input_four,
        ... )
        <Sum4.ar()>
    """
    @classmethod
    def new(cls, *, input_one: UGenRecursiveInput, input_two: UGenRecursiveInput, input_three: UGenRecursiveInput, input_four: UGenRecursiveInput) -> UGenOperable: ...
class Sweep(UGen):
    """
    A triggered linear ramp.
    
    ::
    
        >>> sweep = supriya.ugens.Sweep.ar(
        ...     rate=1,
        ...     trigger=0,
        ... )
        >>> sweep
        <Sweep.ar()[0]>
    """
    @classmethod
    def ar(cls, *, trigger: UGenRecursiveInput = 0, rate: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, trigger: UGenRecursiveInput = 0, rate: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class SyncSaw(UGen):
    """
    A sawtooth wave that is hard synched to a fundamental pitch.
    
    ::
    
        >>> sync_saw = supriya.ugens.SyncSaw.ar(
        ...     saw_frequency=440,
        ...     sync_frequency=440,
        ... )
        >>> sync_saw
        <SyncSaw.ar()[0]>
    """
    @classmethod
    def ar(cls, *, sync_frequency: UGenRecursiveInput = 440.0, saw_frequency: UGenRecursiveInput = 440.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, sync_frequency: UGenRecursiveInput = 440.0, saw_frequency: UGenRecursiveInput = 440.0) -> UGenOperable: ...
class TBall(UGen):
    """
    A bouncing object physical model.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> tball = supriya.ugens.TBall.ar(
        ...     damping=0,
        ...     friction=0.01,
        ...     gravity=10,
        ...     source=source,
        ... )
        >>> tball
        <TBall.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, gravity: UGenRecursiveInput = 10.0, damping: UGenRecursiveInput = 0.0, friction: UGenRecursiveInput = 0.01) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, gravity: UGenRecursiveInput = 10.0, damping: UGenRecursiveInput = 0.0, friction: UGenRecursiveInput = 0.01) -> UGenOperable: ...
class TDelay(UGen):
    """
    A trigger delay.
    
    ::
    
        >>> source = supriya.ugens.Dust.kr(density=1)
        >>> tdelay = supriya.ugens.TDelay.ar(
        ...     duration=0.1,
        ...     source=source,
        ... )
        >>> tdelay
        <TDelay.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, duration: UGenRecursiveInput = 0.1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, duration: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class TExpRand(UGen):
    """
    A triggered exponential random number generator.
    
    ::
    
        >>> trigger = supriya.ugens.Impulse.ar()
        >>> t_exp_rand = supriya.ugens.TExpRand.ar(
        ...     minimum=-1.0,
        ...     maximum=1.0,
        ...     trigger=trigger,
        ... )
        >>> t_exp_rand
        <TExpRand.ar()[0]>
    """
    @classmethod
    def ar(cls, *, minimum: UGenRecursiveInput = 0.01, maximum: UGenRecursiveInput = 1.0, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, minimum: UGenRecursiveInput = 0.01, maximum: UGenRecursiveInput = 1.0, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
class TIRand(UGen):
    """
    A triggered integer random number generator.
    
    ::
    
        >>> trigger = supriya.ugens.Impulse.ar()
        >>> t_i_rand = supriya.ugens.TIRand.ar(
        ...     minimum=0,
        ...     maximum=127,
        ...     trigger=trigger,
        ... )
        >>> t_i_rand
        <TIRand.ar()[0]>
    """
    @classmethod
    def ar(cls, *, minimum: UGenRecursiveInput = 0, maximum: UGenRecursiveInput = 127, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, minimum: UGenRecursiveInput = 0, maximum: UGenRecursiveInput = 127, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
class TRand(UGen):
    """
    A triggered random number generator.
    
    ::
    
        >>> trigger = supriya.ugens.Impulse.ar()
        >>> t_rand = supriya.ugens.TRand.ar(
        ...     minimum=-1.0,
        ...     maximum=1.0,
        ...     trigger=trigger,
        ... )
        >>> t_rand
        <TRand.ar()[0]>
    """
    @classmethod
    def ar(cls, *, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
class TWindex(UGen):
    """
    A triggered windex.
    
    ::
    
        >>> trigger = supriya.ugens.Impulse.ar()
        >>> t_windex = supriya.ugens.TWindex.ar(
        ...     trigger=trigger,
        ...     normalize=0,
        ...     array=[1, 2, 3],
        ... )
        >>> t_windex
        <TWindex.ar()[0]>
    """
    @classmethod
    def ar(cls, *, trigger: UGenRecursiveInput, normalize: UGenRecursiveInput = 0, array: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, trigger: UGenRecursiveInput, normalize: UGenRecursiveInput = 0, array: UGenRecursiveInput) -> UGenOperable: ...
class ToggleFF(UGen):
    """
    A toggle flip-flop.
    
    ::
    
        >>> trigger = supriya.ugens.Dust.kr(density=1)
        >>> toggle_ff = supriya.ugens.ToggleFF.ar(
        ...     trigger=trigger,
        ... )
        >>> toggle_ff
        <ToggleFF.ar()[0]>
    """
    @classmethod
    def ar(cls, *, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, trigger: UGenRecursiveInput = 0) -> UGenOperable: ...
class Trig(UGen):
    """
    A timed trigger.
    
    ::
    
        >>> source = supriya.ugens.Dust.kr(density=1)
        >>> trig = supriya.ugens.Trig.ar(
        ...     duration=0.1,
        ...     source=source,
        ... )
        >>> trig
        <Trig.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, duration: UGenRecursiveInput = 0.1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, duration: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class Trig1(UGen):
    """
    A timed trigger.
    
    ::
    
        >>> source = supriya.ugens.Dust.kr(density=1)
        >>> trig_1 = supriya.ugens.Trig1.ar(
        ...     duration=0.1,
        ...     source=source,
        ... )
        >>> trig_1
        <Trig1.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, duration: UGenRecursiveInput = 0.1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, duration: UGenRecursiveInput = 0.1) -> UGenOperable: ...
class TrigControl(UGen):
    """
    A UGen: a "unit generator".
    """
    ...
class TwoPole(UGen):
    """
    A two pole filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> two_pole = supriya.ugens.TwoPole.ar(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=source,
        ... )
        >>> two_pole
        <TwoPole.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, radius: UGenRecursiveInput = 0.8) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, radius: UGenRecursiveInput = 0.8) -> UGenOperable: ...
class TwoZero(UGen):
    """
    A two zero filter.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> two_zero = supriya.ugens.TwoZero.ar(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=source,
        ... )
        >>> two_zero
        <TwoZero.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, radius: UGenRecursiveInput = 0.8) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, radius: UGenRecursiveInput = 0.8) -> UGenOperable: ...
class UnaryOpUGen(UGen):
    """
    A UGen: a "unit generator".
    """
    ...
class VDiskIn(UGen):
    """
    Streams in audio from a file, with variable rate.
    
    ::
    
        >>> buffer_id = 23
        >>> vdisk_in = supriya.ugens.VDiskIn.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     loop=0,
        ...     rate=1,
        ...     send_id=0,
        ... )
        >>> vdisk_in
        <VDiskIn.ar()>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, rate: UGenRecursiveInput = 1.0, loop: UGenRecursiveInput = 0, send_id: UGenRecursiveInput = 0, channel_count: int = 1) -> UGenOperable: ...
class VOsc(UGen):
    """
    A wavetable lookup oscillator which can be swept smoothly across wavetables.
    
    ::
    
        >>> vosc = supriya.ugens.VOsc.ar(
        ...     buffer_id=supriya.ugens.MouseX.kr(minimum=0, maximum=7),
        ...     frequency=440,
        ...     phase=0,
        ... )
        >>> vosc
        <VOsc.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, frequency: UGenRecursiveInput = 440.0, phase: UGenRecursiveInput = 0.0) -> UGenOperable: ...
class VOsc3(UGen):
    """
    A wavetable lookup oscillator which can be swept smoothly across wavetables.
    
    ::
    
        >>> vosc_3 = supriya.ugens.VOsc3.ar(
        ...     buffer_id=supriya.ugens.MouseX.kr(minimum=0, maximum=7),
        ...     freq_1=110,
        ...     freq_2=220,
        ...     freq_3=440,
        ... )
        >>> vosc_3
        <VOsc3.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, freq_1: UGenRecursiveInput = 110.0, freq_2: UGenRecursiveInput = 220.0, freq_3: UGenRecursiveInput = 440.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, freq_1: UGenRecursiveInput = 110.0, freq_2: UGenRecursiveInput = 220.0, freq_3: UGenRecursiveInput = 440.0) -> UGenOperable: ...
class VarSaw(UGen):
    """
    A sawtooth-triangle oscillator with variable duty.
    
    ::
    
        >>> supriya.ugens.VarSaw.ar()
        <VarSaw.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0, width: UGenRecursiveInput = 0.5) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 440.0, initial_phase: UGenRecursiveInput = 0.0, width: UGenRecursiveInput = 0.5) -> UGenOperable: ...
class Vibrato(UGen):
    """
    Vibrato is a slow frequency modulation.
    
    ::
    
        >>> vibrato = supriya.ugens.Vibrato.ar(
        ...     delay=0,
        ...     depth=0.02,
        ...     depth_variation=0.1,
        ...     frequency=440,
        ...     initial_phase=0,
        ...     onset=0,
        ...     rate=6,
        ...     rate_variation=0.04,
        ... )
        >>> vibrato
        <Vibrato.ar()[0]>
    """
    @classmethod
    def ar(cls, *, frequency: UGenRecursiveInput = 440, rate: UGenRecursiveInput = 6, depth: UGenRecursiveInput = 0.02, delay: UGenRecursiveInput = 0, onset: UGenRecursiveInput = 0, rate_variation: UGenRecursiveInput = 0.04, depth_variation: UGenRecursiveInput = 0.1, initial_phase: UGenRecursiveInput = 0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, frequency: UGenRecursiveInput = 440, rate: UGenRecursiveInput = 6, depth: UGenRecursiveInput = 0.02, delay: UGenRecursiveInput = 0, onset: UGenRecursiveInput = 0, rate_variation: UGenRecursiveInput = 0.04, depth_variation: UGenRecursiveInput = 0.1, initial_phase: UGenRecursiveInput = 0) -> UGenOperable: ...
class Warp1(UGen):
    """
    ::
    
        >>> warp_1 = supriya.ugens.Warp1.ar(
        ...     buffer_id=0,
        ...     channel_count=1,
        ...     envelope_buffer_id=-1,
        ...     frequency_scaling=1,
        ...     interpolation=1,
        ...     overlaps=8,
        ...     pointer=0,
        ...     window_rand_ratio=0,
        ...     window_size=0.2,
        ... )
        >>> warp_1
        <Warp1.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput = 0, pointer: UGenRecursiveInput = 0, frequency_scaling: UGenRecursiveInput = 1, window_size: UGenRecursiveInput = 0.2, envelope_buffer_id: UGenRecursiveInput = -1, overlaps: UGenRecursiveInput = 8, window_rand_ratio: UGenRecursiveInput = 0, interpolation: UGenRecursiveInput = 1, channel_count: int = 1) -> UGenOperable: ...
class WhiteNoise(UGen):
    """
    A white noise unit generator.
    
    ::
    
        >>> supriya.ugens.WhiteNoise.ar()
        <WhiteNoise.ar()[0]>
    """
    @classmethod
    def ar(cls) -> UGenOperable: ...
    @classmethod
    def kr(cls) -> UGenOperable: ...
class Wrap(UGen):
    """
    Wraps a signal outside given thresholds.
    
    ::
    
        >>> source = supriya.ugens.SinOsc.ar()
        >>> wrap = supriya.ugens.Wrap.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ... )
        >>> wrap
        <Wrap.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
    @classmethod
    def ir(cls, *, source: UGenRecursiveInput, minimum: UGenRecursiveInput = 0.0, maximum: UGenRecursiveInput = 1.0) -> UGenOperable: ...
class WrapIndex(UGen):
    """
    A wrapping buffer indexer.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> wrap_index = supriya.ugens.WrapIndex.ar(
        ...     buffer_id=23,
        ...     source=source,
        ... )
        >>> wrap_index
        <WrapIndex.ar()[0]>
    """
    @classmethod
    def ar(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, buffer_id: UGenRecursiveInput, source: UGenRecursiveInput) -> UGenOperable: ...
class XFade2(UGen):
    """
    Two channel equal power crossfader.
    
    ::
    
        >>> xfade_3 = supriya.ugens.XFade2.ar(
        ...     in_a=supriya.ugens.Saw.ar(),
        ...     in_b=supriya.ugens.SinOsc.ar(),
        ...     level=1,
        ...     pan=supriya.ugens.LFTri.kr(frequency=0.1),
        ... )
        >>> xfade_3
        <XFade2.ar()[0]>
    """
    @classmethod
    def ar(cls, *, in_a: UGenRecursiveInput, in_b: UGenRecursiveInput = 0, pan: UGenRecursiveInput = 0, level: UGenRecursiveInput = 1) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, in_a: UGenRecursiveInput, in_b: UGenRecursiveInput = 0, pan: UGenRecursiveInput = 0, level: UGenRecursiveInput = 1) -> UGenOperable: ...
class XLine(UGen):
    """
    An exponential line generating unit generator.
    
    ::
    
        >>> supriya.ugens.XLine.ar()
        <XLine.ar()[0]>
    """
    @classmethod
    def ar(cls, *, start: UGenRecursiveInput = 0.0, stop: UGenRecursiveInput = 0.0, duration: UGenRecursiveInput = 1.0, done_action: UGenRecursiveInput = DoneAction.NOTHING) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, start: UGenRecursiveInput = 0.0, stop: UGenRecursiveInput = 0.0, duration: UGenRecursiveInput = 1.0, done_action: UGenRecursiveInput = DoneAction.NOTHING) -> UGenOperable: ...
class XOut(UGen):
    """
    A cross-fading bus output unit generator.
    
    ::
    
        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> xout = supriya.ugens.XOut.ar(
        ...     bus=0,
        ...     crossfade=0.5,
        ...     source=source,
        ... )
        >>> xout
        <XOut.ar()>
    """
    @classmethod
    def ar(cls, *, bus: UGenRecursiveInput = 0, crossfade: UGenRecursiveInput = 0.0, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, bus: UGenRecursiveInput = 0, crossfade: UGenRecursiveInput = 0.0, source: UGenRecursiveInput) -> UGenOperable: ...
class ZeroCrossing(UGen):
    """
    A zero-crossing frequency follower.
    
    ::
    
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> zero_crossing = supriya.ugens.ZeroCrossing.ar(
        ...     source=source,
        ... )
        >>> zero_crossing
        <ZeroCrossing.ar()[0]>
    """
    @classmethod
    def ar(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
    @classmethod
    def kr(cls, *, source: UGenRecursiveInput) -> UGenOperable: ...
