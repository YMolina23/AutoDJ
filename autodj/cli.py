import argparse
from pathlib import Path

from .models import Config
from .pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AutoDJ LangGraph pipeline")
    parser.add_argument(
        "--songs-dir",
        default="Canciones",
        help="Folder with audio files",
    )
    parser.add_argument(
        "--seconds-per-track",
        type=int,
        default=40,
        help="Seconds to use from each track",
    )
    parser.add_argument(
        "--crossfade-sec",
        type=int,
        default=8,
        help="Seconds for crossfade transitions",
    )
    parser.add_argument(
        "--analysis-seconds",
        type=int,
        default=90,
        help="Seconds to analyze for BPM",
    )
    parser.add_argument(
        "--output",
        default=str(Path("output") / "mix.mp3"),
        help="Output mix file",
    )
    parser.add_argument(
        "--report",
        default=str(Path("output") / "mix_report.json"),
        help="Output report JSON",
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = Config(
        songs_dir=args.songs_dir,
        seconds_per_track=max(1, args.seconds_per_track),
        crossfade_sec=max(0, args.crossfade_sec),
        output_path=args.output,
        report_path=args.report,
        bpm_analysis_seconds=max(10, args.analysis_seconds),
    )

    state = run_pipeline(config)
    print("Mix exported:", state["mix_path"])
    print("Report exported:", state["report_path"])


if __name__ == "__main__":
    main()
