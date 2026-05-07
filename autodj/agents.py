from pathlib import Path

from .audio_tools import (
    analyze_bpm,
    build_mix,
    export_mix,
    list_audio_files,
    order_tracks_smooth_bpm,
    write_report,
)
from .models import AutoDJState, TrackInfo


def ingest_agent(state: AutoDJState) -> dict:
    songs_dir = state["config"].songs_dir
    track_paths = list_audio_files(songs_dir)
    if not track_paths:
        raise ValueError(f"No audio files found in {songs_dir}")

    return {"track_paths": track_paths}


def bpm_agent(state: AutoDJState) -> dict:
    config = state["config"]
    tracks = []

    for path in state["track_paths"]:
        title = Path(path).stem
        bpm, duration = analyze_bpm(path, config.bpm_analysis_seconds)
        tracks.append(TrackInfo(path=path, title=title, bpm=bpm, duration_sec=duration))

    return {"tracks": tracks}


def plan_agent(state: AutoDJState) -> dict:
    ordered = order_tracks_smooth_bpm(state["tracks"])
    return {"ordered_tracks": ordered}


def mix_agent(state: AutoDJState) -> dict:
    config = state["config"]
    mix = build_mix(
        state["ordered_tracks"],
        config.seconds_per_track,
        config.crossfade_sec,
    )

    output_path = config.output_path
    report_path = config.report_path

    write_report(state["ordered_tracks"], report_path)
    export_mix(mix, output_path)

    return {"mix_path": output_path, "report_path": report_path}


