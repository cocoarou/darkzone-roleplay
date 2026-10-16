#!/usr/bin/env python3
"""Render the Skarheim narration slideshow to an MP4 with FFmpeg."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FPS = 30
WIDTH = 1920
HEIGHT = 1080
TOTAL_FRAMES = 4772
FADE_FRAMES = 60
DEFAULT_ANIMATIONS_DIR = ROOT / "output/video/ai/loops-slow-40s"

# Frame values mark when each incoming animation reaches full opacity.
SHOTS = [
    ("ls_1-loop-40s.mp4", 0),
    ("ls_2-loop-40s.mp4", 195),
    ("ls_3-loop-40s.mp4", 360),
    ("ls_4-loop-40s.mp4", 525),
    ("brunilda-loop-40s.mp4", 690),
    ("ls_7-loop-40s.mp4", 1186),
    ("dummy_4-loop-40s.mp4", 2177),
    ("yldra_1-loop-40s.mp4", 2370),
    ("ls_8-loop-40s.mp4", 2689),
    ("ls_9-loop-40s.mp4", 2927),
    ("ls_10-loop-40s.mp4", 3165),
    ("valakit_1-loop-40s.mp4", 3403),
    ("astrid_1-loop-40s.mp4", 4090),
]


def timecode(frame: int) -> str:
    return f"{frame / FPS:.6f}"


def frame_lengths() -> list[int]:
    starts = [0, *(frame - FADE_FRAMES // 2 for _, frame in SHOTS[1:])]
    lengths = []
    for index, start in enumerate(starts):
        next_start = starts[index + 1] if index + 1 < len(starts) else TOTAL_FRAMES
        lengths.append(next_start - start)
    return lengths


def resolve_ffmpeg(requested: str | None) -> str:
    if requested:
        return requested
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("FFmpeg was not found. Install FFmpeg or pass --ffmpeg /path/to/ffmpeg.")
    return ffmpeg


def render(ffmpeg: str, output: Path, animations_dir: Path) -> None:
    audio = ROOT / "resources/audio/avventura-doppiata-musica.mp3"
    if not audio.is_file():
        raise SystemExit(f"Missing narration audio: {audio}")

    lengths = frame_lengths()
    filter_parts = []
    command = [ffmpeg, "-hide_banner", "-y"]

    for filename, _ in SHOTS:
        animation = animations_dir / filename
        if not animation.is_file():
            raise SystemExit(f"Missing animation: {animation}")
        command.extend(["-stream_loop", "-1", "-i", str(animation)])

    audio_input = len(SHOTS)
    command.extend(["-i", str(audio)])

    for index, ((_, _), length) in enumerate(zip(SHOTS, lengths)):
        source = f"[{index}:v]"
        raw_bg, raw_fg = f"bgraw{index}", f"fgraw{index}"
        bg, fg, composed = f"bg{index}", f"fg{index}", f"composed{index}"
        output_label = f"v{index}"
        filter_parts.append(
            f"{source}fps={FPS},trim=end_frame={length},setpts=PTS-STARTPTS,"
            f"split=2[{raw_bg}][{raw_fg}]"
        )
        filter_parts.append(
            f"[{raw_bg}]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},boxblur=24:12,eq=brightness=-0.22:saturation=0.85[{bg}]"
        )
        filter_parts.append(
            f"[{raw_fg}]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease[{fg}]"
        )
        filter_parts.append(
            f"[{bg}][{fg}]overlay=(W-w)/2:(H-h)/2,"
            f"format=yuv420p,setsar=1[{composed}]"
        )
        fade_source = f"[{composed}]"
        fade_in_frames = FADE_FRAMES if index == 0 else FADE_FRAMES // 2
        fade_out_frames = FADE_FRAMES if index == len(SHOTS) - 1 else FADE_FRAMES // 2
        fade_start = length - fade_out_frames
        filter_parts.append(
            f"{fade_source}fade=t=in:st=0:d={timecode(fade_in_frames)}:color=black,"
            f"fade=t=out:st={timecode(fade_start)}:d={timecode(fade_out_frames)}:color=black,"
            f"trim=end_frame={length},setpts=PTS-STARTPTS,setsar=1,"
            f"format=yuv420p,settb=expr=1/{FPS}[{output_label}]"
        )

    joined = "".join(f"[v{index}]" for index in range(len(SHOTS)))
    filter_parts.append(f"{joined}concat=n={len(SHOTS)}:v=1:a=0[vout]")
    filter_parts.append(
        f"[{audio_input}:a]aresample=48000:async=1:first_pts=0[aout]"
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    command.extend([
        "-filter_complex", ";".join(filter_parts),
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "192k",
        "-t", timecode(TOTAL_FRAMES), "-movflags", "+faststart",
        "-metadata", "title=Skarheim - Avventura",
        "-metadata", "comment=Animazioni sincronizzate alla narrazione",
        str(output),
    ])
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ffmpeg",
        help="FFmpeg executable (defaults to ffmpeg from PATH).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "output/video/slideshow/avventura-slideshow-animazioni-rallentate-40s.mp4",
        help="Output MP4 path.",
    )
    parser.add_argument(
        "--animations-dir",
        type=Path,
        default=DEFAULT_ANIMATIONS_DIR,
        help=f"Directory containing the 40-second animation loops (default: {DEFAULT_ANIMATIONS_DIR}).",
    )
    args = parser.parse_args()
    render(
        resolve_ffmpeg(args.ffmpeg),
        args.output.expanduser().resolve(),
        args.animations_dir.expanduser().resolve(),
    )


if __name__ == "__main__":
    main()
