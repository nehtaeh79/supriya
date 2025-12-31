import random
import textwrap
from pathlib import Path

import pytest

from scripts import piano_sampler


class DummyContext:
    def __init__(self) -> None:
        self.synth_calls = []
        self._time = None

    def at(self, time: float):
        self._time = time
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self._time = None

    def add_synth(self, synth, **kwargs):
        self.synth_calls.append({"time": self._time, "synth": synth, **kwargs})


def test_parse_midicsv_single_note(tmp_path: Path) -> None:
    csv_text = textwrap.dedent(
        """
        0, 0, Header, 1, 1, 480
        1, 0, Tempo, 500000
        1, 0, Note_on_c, 0, 60, 64
        1, 480, Note_off_c, 0, 60, 0
        1, 480, End_track
        0, 0, End_of_file
        """
    ).strip()
    csv_path = tmp_path / "phrase.csv"
    csv_path.write_text(csv_text)

    events = piano_sampler.parse_midicsv_file(csv_path)

    assert len(events) == 1
    event = events[0]
    assert event.start == 0.0
    assert event.duration == pytest.approx(0.5)
    assert event.note == 60
    assert event.velocity == 64


def test_parse_midi_file_with_tempo_change(tmp_path: Path) -> None:
    mido = pytest.importorskip("mido")
    midi = mido.MidiFile(ticks_per_beat=480)
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("set_tempo", tempo=600000, time=0))
    track.append(mido.Message("note_on", note=60, velocity=64, time=0))
    track.append(mido.Message("note_off", note=60, velocity=0, time=480))
    track.append(mido.MetaMessage("set_tempo", tempo=300000, time=0))
    track.append(mido.Message("note_on", note=62, velocity=100, time=240))
    track.append(mido.Message("note_off", note=62, velocity=0, time=240))
    midi.tracks.append(track)
    midi_path = tmp_path / "phrase.mid"
    midi.save(midi_path)

    events = piano_sampler.parse_midi_file(midi_path)

    assert [e.note for e in events] == [60, 62]
    assert [e.velocity for e in events] == [64, 100]
    assert events[0].start == 0.0
    assert events[0].duration == pytest.approx(0.6)
    assert events[1].start == pytest.approx(0.75)
    assert events[1].duration == pytest.approx(0.15)


def test_load_sample_buffers_real_time_chunks(monkeypatch, tmp_path: Path) -> None:
    sample_pack = tmp_path / "samples"
    sample_pack.mkdir()
    for i in range(3):
        (sample_pack / f"{i}.wav").touch()

    calls = []

    class FakeServer:
        def add_synthdefs(self, synth):
            calls.append(("synthdefs", synth))

        def add_buffer(self, file_path):
            calls.append(("buffer", file_path.name))
            return f"buf-{file_path.name}"

        def at(self, *_args, **_kwargs):
            raise AssertionError("real-time loading should not bundle via at()")

    buffers = piano_sampler.load_sample_buffers(FakeServer(), sample_pack)

    assert len(buffers) == 3
    assert calls[0][0] == "synthdefs"
    assert [c for c in calls if c[0] == "buffer"] == [
        ("buffer", "0.wav"),
        ("buffer", "1.wav"),
        ("buffer", "2.wav"),
    ]


def test_parse_claire_de_lune_midi_snapshot() -> None:
    midi_path = Path(__file__).resolve().parents[2] / "scripts" / "midi" / "claire_de_lune.mid"
    events = piano_sampler.parse_midi_file(midi_path)

    assert 1000 < len(events) < 5000
    first_three = [
        (0.625, 0.634765625, 65, 39),
        (0.625, 0.634765625, 68, 39),
        (1.25, 1.9583305, 77, 61),
    ]
    for event, (start, duration, note, velocity) in zip(events[:3], first_three):
        assert event.start == pytest.approx(start, rel=1e-6)
        assert event.duration == pytest.approx(duration, rel=1e-6)
        assert event.note == note
        assert event.velocity == velocity

    starts = [event.start for event in events]
    assert min(starts) >= 0.0
    assert max(starts) == pytest.approx(234.1803405, rel=1e-6)
    assert min(event.note for event in events) >= piano_sampler.NOTE_RANGE.start
    assert max(event.note for event in events) <= piano_sampler.NOTE_RANGE.stop


def test_schedule_pattern_enqueues_expected_notes(monkeypatch) -> None:
    monkeypatch.setattr(piano_sampler.time, "time", lambda: 0.0)
    indices, pitches, max_dynamic = piano_sampler.build_lookup(quiet=True)
    buffers = [f"buf-{i}" for i in range(max(indices) + 1)]
    context = DummyContext()
    rng = random.Random(1234)

    end_time = piano_sampler.schedule_pattern(
        context,
        buffers,
        indices,
        pitches,
        max_dynamic,
        start_time=0.0,
        duration=0.5,
        notes=[piano_sampler.NOTE_RANGE.start, piano_sampler.NOTE_RANGE.start + 1],
        durs=[0.25],
        dynamics=[0],
        amps=[0.5, 1.0],
        rel=1.0,
        pan_range=(-0.1, 0.1),
        rng=rng,
    )

    assert end_time == pytest.approx(1.5)
    assert [call["time"] for call in context.synth_calls] == [0.0, 0.25]

    first_note = float(piano_sampler.NOTE_RANGE.start)
    second_note = float(piano_sampler.NOTE_RANGE.start + 1)
    expected = [
        piano_sampler.select_sample(first_note, 0, indices, pitches, max_dynamic),
        piano_sampler.select_sample(second_note, 0, indices, pitches, max_dynamic),
    ]
    for call, (sample_index, rate) in zip(context.synth_calls, expected):
        assert call["buf"] == buffers[sample_index]
        assert call["rate"] == rate
        assert -0.1 <= call["pan"] <= 0.1


def test_schedule_note_events_sorts_by_start_time(monkeypatch) -> None:
    monkeypatch.setattr(piano_sampler.time, "time", lambda: 0.0)
    indices, pitches, max_dynamic = piano_sampler.build_lookup(quiet=True)
    buffers = [f"buf-{i}" for i in range(max(indices) + 1)]
    context = DummyContext()
    rng = random.Random(0)
    events = [
        piano_sampler.NoteEvent(start=1.0, duration=0.1, note=62, velocity=80),
        piano_sampler.NoteEvent(start=0.2, duration=0.1, note=60, velocity=80),
        piano_sampler.NoteEvent(start=0.5, duration=0.1, note=64, velocity=80),
    ]

    piano_sampler.schedule_note_events(
        context,
        buffers,
        indices,
        pitches,
        max_dynamic,
        events,
        start_time=0.0,
        pan_range=(0.0, 0.0),
        rng=rng,
    )

    assert [call["time"] for call in context.synth_calls] == [0.2, 0.5, 1.0]


def test_realtime_schedule_uses_absolute_time(monkeypatch) -> None:
    indices, pitches, max_dynamic = piano_sampler.build_lookup(quiet=True)
    buffers = [f"buf-{i}" for i in range(max(indices) + 1)]

    class RTContext(DummyContext):
        pass

    rt_context = RTContext()
    monkeypatch.setattr(piano_sampler.time, "time", lambda: 1000.0)
    rng = random.Random(0)

    piano_sampler.schedule_note_events(
        rt_context,
        buffers,
        indices,
        pitches,
        max_dynamic,
        [
            piano_sampler.NoteEvent(start=0.0, duration=0.1, note=60, velocity=80),
            piano_sampler.NoteEvent(start=0.5, duration=0.1, note=62, velocity=80),
        ],
        start_time=0.1,
        pan_range=(0.0, 0.0),
        rng=rng,
    )

    assert rt_context.synth_calls[0]["time"] == pytest.approx(1000.1)
    assert rt_context.synth_calls[1]["time"] == pytest.approx(1000.6)


def test_load_note_events_rejects_unknown_extension(tmp_path: Path) -> None:
    path = tmp_path / "notes.txt"
    path.write_text("invalid")
    with pytest.raises(ValueError, match="Unsupported MIDI file extension"):
        piano_sampler.load_note_events(path)


def test_realtime_options_node_budget_scales() -> None:
    opts_small = piano_sampler.realtime_options(10)
    opts_large = piano_sampler.realtime_options(2000)
    assert opts_small.maximum_node_count >= piano_sampler.MIN_REALTIME_NODE_BUDGET
    assert opts_large.maximum_node_count >= 8000
    assert opts_large.maximum_node_count > opts_small.maximum_node_count
