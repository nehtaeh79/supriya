import textwrap
import contextlib
from pathlib import Path

import pytest

from scripts import drum_sampler


def test_samples_exist():
    # Basic sanity: all referenced sample filenames should exist on disk.
    missing = []
    for instrument in drum_sampler.INSTRUMENTS.values():
        for layer in instrument.layers:
            if not layer.path.exists():
                missing.append(layer.path.name)
    assert not missing, f"missing samples: {missing}"


def test_load_kit_batches_buffer_allocations_for_realtime():
    class FakeBuffer:
        def __init__(self, id_: int):
            self.id_ = id_

        def __float__(self) -> float:
            return float(self.id_)

        def __int__(self) -> int:
            return self.id_

    class FakeContext:
        def __init__(self):
            self.batches: list[list[Path]] = []
            self._current: list[Path] | None = None
            self._next_buffer_id = 0

        @contextlib.contextmanager
        def at(self, seconds=None):
            self._current = []
            yield
            self.batches.append(self._current)
            self._current = None

        def add_synthdefs(self, *args, **kwargs):
            return None

        def add_buffer(self, *, file_path: Path, **kwargs):
            assert self._current is not None
            self._next_buffer_id += 1
            self._current.append(file_path)
            return FakeBuffer(self._next_buffer_id)

    context = FakeContext()
    kit = drum_sampler.load_kit(context, at=None)
    assert "kick_open" in kit.layers
    assert len(context.batches) > 1
    max_batch = max(len(batch) for batch in context.batches)
    assert max_batch <= drum_sampler.REALTIME_BUFFER_LOAD_BATCH_SIZE


def test_load_mono_buffers_reads_left_channel(monkeypatch):
    calls: list[tuple[Path, list[int] | None]] = []

    class FakeBuffer:
        def __init__(self, id_: int):
            self.id_ = id_

        def __float__(self) -> float:
            return float(self.id_)

        def __int__(self) -> int:
            return self.id_

    class FakeServer:
        def __init__(self):
            self._next_buffer_id = 0

        @contextlib.contextmanager
        def at(self, seconds=None):
            yield

        def add_buffer(self, *, file_path: Path, channel_indices=None, **kwargs):
            calls.append((file_path, channel_indices))
            self._next_buffer_id += 1
            return FakeBuffer(self._next_buffer_id)

    def fake_wait_for_buffers_loaded(_server, _buffers, *, timeout=30.0):
        return None

    monkeypatch.setattr(drum_sampler, "_wait_for_buffers_loaded", fake_wait_for_buffers_loaded)

    server = FakeServer()
    path_a = Path("a.wav")
    path_b = Path("b.wav")
    buffers = drum_sampler._load_mono_buffers(server, [path_a, path_b, path_a])
    assert [path for path, _indices in calls] == [path_a, path_b]
    assert all(indices == [0] for _path, indices in calls)
    assert set(buffers) == {path_a, path_b}


def test_default_mapping_includes_core_notes():
    mapping = drum_sampler.default_mapping()
    # Kick and snare defaults align with GM percussion expectations.
    assert mapping[36] == "kick_open"
    assert mapping[38] in {"snare_bright", "snare_warm"}
    # Hat-like notes mapped to stick/hand drums for convenience.
    assert mapping[42] == "ethnic_stick"
    assert mapping[46] == "ethnic_low_open"


def test_apply_mapping_overrides_validation():
    base = {36: "kick_open"}
    with pytest.raises(ValueError):
        drum_sampler.apply_mapping_overrides(base, ["36=unknown"])
    updated = drum_sampler.apply_mapping_overrides(base, ["36=kick_muted"])
    assert updated[36] == "kick_muted"


def test_convert_ticks_to_seconds_with_tempo_change():
    events = [(0, 36, 100), (480, 38, 100)]
    tempos = [(0, 500_000), (480, 250_000)]  # tempo doubles after first beat
    timed = drum_sampler.convert_ticks_to_seconds(events, tempos, ticks_per_beat=480)
    # First event at time 0, tempo change applies before the second event so it lands at 0.5s.
    assert timed[0][0] == 0.0
    assert pytest.approx(timed[1][0], rel=1e-6) == 0.5


def test_parse_midicsv_round_trip(tmp_path: Path):
    csv_text = textwrap.dedent(
        """
        0, 0, Header, 1, 2, 480
        1, 0, Tempo, 600000
        1, 1, Note_on_c, 0, 36, 100
        1, 241, Note_on_c, 0, 38, 127
        1, 480, End_of_file
        """
    ).strip()
    csv_path = tmp_path / "seq.csv"
    csv_path.write_text(csv_text)
    events, tempos, tpq = drum_sampler.parse_midicsv(csv_path)
    assert tpq == 480
    assert tempos == [(0, 600000)]
    assert events == [(1, 36, 100), (241, 38, 127)]


def test_build_events_from_notes_orders_and_zeroes():
    mapping = {36: "kick_open", 38: "snare_bright"}
    timed = [(0.25, 38, 90), (0.1, 36, 80)]
    events = drum_sampler.build_events_from_notes(timed, mapping)
    # Times are offset to start at zero and sorted.
    assert [e.instrument for e in events] == ["kick_open", "snare_bright"]
    assert [pytest.approx(e.time, rel=1e-6) for e in events] == [0.0, 0.15]


def test_demo_events_all_includes_all_instruments():
    events = drum_sampler.demo_events("all")
    assert len(events) == len(drum_sampler.INSTRUMENTS)
    assert {e.instrument for e in events} == set(drum_sampler.INSTRUMENTS.keys())


def test_program_registry_contains_ambient_01():
    assert "ambient_01" in drum_sampler.PROGRAMS
    assert drum_sampler.PROGRAMS["ambient_01"].implemented is True
