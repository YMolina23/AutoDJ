from dataclasses import dataclass
from typing import List, TypedDict


@dataclass
class Config:
    songs_dir: str
    seconds_per_track: int
    crossfade_sec: int
    output_path: str
    report_path: str
    bpm_analysis_seconds: int


@dataclass
class TrackInfo:
    path: str
    title: str
    bpm: float
    duration_sec: float


class AutoDJState(TypedDict):
    config: Config
    track_paths: List[str]
    tracks: List[TrackInfo]
    ordered_tracks: List[TrackInfo]
    mix_path: str
    report_path: str
