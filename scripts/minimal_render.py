"""
Render a short sine tone using a non-realtime Score.

Note: SuperCollider's scsynth must be installed and available on your PATH
for non-realtime rendering to work.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import supriya
from supriya import Envelope, synthdef
from supriya.ugens import EnvGen, Out, SinOsc


@synthdef()
def simple_sine(frequency=440, amplitude=0.2):
    sine = SinOsc.ar(frequency=frequency) * amplitude
    envelope = EnvGen.kr(
        envelope=Envelope.percussive(attack_time=0.01, release_time=0.3),
        done_action=2,
    )
    Out.ar(bus=0, source=[sine * envelope] * 2)


def render(output_path: Path) -> tuple[Path | None, int]:
    score = supriya.Score(output_bus_channel_count=2)
    with score.at(0):
        score.add_synthdefs(simple_sine)
        score.add_synth(simple_sine, frequency=440)
    with score.at(1.0):
        score.do_nothing()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return supriya.render(score, output_file_path=output_path, header_format="wav")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a short sine tone to WAV")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("output") / "minimal_render.wav",
        help="Output WAV file path (default: scripts/output/minimal_render.wav)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path, exit_code = render(args.output)
    if output_path:
        print(f"Rendered to {output_path}")
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
