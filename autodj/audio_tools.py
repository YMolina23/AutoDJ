import json
from pathlib import Path
from typing import Iterable, List, Tuple

import librosa
import numpy as np
from pydub import AudioSegment, effects

from .models import TrackInfo


AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"}


def list_audio_files(songs_dir: str) -> List[str]:
    base = Path(songs_dir)
    if not base.exists():
        raise FileNotFoundError(f"Songs directory not found: {songs_dir}")

    files = [str(p) for p in base.iterdir() if p.suffix.lower() in AUDIO_EXTENSIONS]
    files.sort()
    return files


def analyze_bpm(path: str, analysis_seconds: int) -> Tuple[float, float]:
    y, sr = librosa.load(path, mono=True, duration=analysis_seconds)
    if y.size == 0:
        return 0.0, 0.0

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    duration = float(librosa.get_duration(path=path))
    tempo_array = np.asarray(tempo)
    tempo_value = float(tempo_array) if tempo_array.ndim == 0 else float(tempo_array.mean())
    return tempo_value, duration


def order_tracks_smooth_bpm(tracks: Iterable[TrackInfo]) -> List[TrackInfo]:
    remaining = list(tracks)
    if not remaining:
        return []

    remaining.sort(key=lambda t: t.bpm)
    start_index = len(remaining) // 2
    ordered = [remaining.pop(start_index)]

    while remaining:
        last_bpm = ordered[-1].bpm
        next_index = min(
            range(len(remaining)),
            key=lambda i: abs(remaining[i].bpm - last_bpm),
        )
        ordered.append(remaining.pop(next_index))

    return ordered


def _prepare_segment(path: str, seconds_per_track: int) -> AudioSegment:
    audio = AudioSegment.from_file(path)
    segment_ms = max(0, seconds_per_track * 1000)
    if segment_ms > 0:
        audio = audio[:segment_ms]

    audio = effects.normalize(audio)
    return audio.fade_in(300).fade_out(300)


def build_mix(
    ordered_tracks: Iterable[TrackInfo],
    seconds_per_track: int,
    crossfade_sec: int,
) -> AudioSegment:
    mix = None
    base_crossfade_ms = max(0, crossfade_sec * 1000)

    for track in ordered_tracks:
        segment = _prepare_segment(track.path, seconds_per_track)
        if mix is None:
            mix = segment
            continue

        crossfade_ms = min(base_crossfade_ms, len(segment), len(mix))
        if crossfade_ms <= 0:
            mix = mix.append(segment, crossfade=0)
        else:
            mix = mix.append(segment, crossfade=crossfade_ms)

    if mix is None:
        raise ValueError("No audio segments to mix")

    return mix


def export_mix(mix: AudioSegment, output_path: str) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    mix.export(output, format=output.suffix.lstrip("."))


def load_audio(path: str) -> AudioSegment:
    return AudioSegment.from_file(path)


def write_report(tracks: Iterable[TrackInfo], report_path: str) -> None:
    payload = [
        {
            "title": track.title,
            "bpm": round(track.bpm, 2),
            "duration_sec": round(track.duration_sec, 2),
            "path": track.path,
        }
        for track in tracks
    ]

    report = Path(report_path)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
