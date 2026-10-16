#!/usr/bin/env python3
"""Create a slowed, forward-only loop without changing the source aspect ratio."""

from __future__ import annotations

import argparse
import io
import shutil
import subprocess
from pathlib import Path

from PIL import Image


FPS = 16


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Source animation MP4.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Destination MP4 (defaults to <input-stem>-forward-loop.mp4).",
    )
    parser.add_argument(
        "--seconds",
        type=int,
        default=40,
        help="Loop duration in seconds (default: 40).",
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=2,
        help="Number of forward periods in the loop (default: 2).",
    )
    parser.add_argument(
        "--slowdown",
        type=float,
        default=4.4,
        help="Slowdown factor before crossfading (default: 4.4).",
    )
    parser.add_argument("--ffmpeg", help="FFmpeg executable (defaults to PATH).")
    return parser.parse_args()


def resolve_ffmpeg(requested: str | None) -> str:
    if requested:
        return requested
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("FFmpeg was not found. Install FFmpeg or pass --ffmpeg /path/to/ffmpeg.")
    return ffmpeg


def decode_frames(
    ffmpeg: str,
    source: Path,
    slowdown: float,
) -> tuple[list[Image.Image], int, int]:
    first_frame = subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(source),
            "-frames:v",
            "1",
            "-f",
            "image2pipe",
            "-vcodec",
            "png",
            "-",
        ],
        check=True,
        capture_output=True,
    ).stdout
    with Image.open(io.BytesIO(first_frame)) as image:
        width, height = image.size

    decoded = subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(source),
            "-vf",
            f"setpts={slowdown}*PTS,"
            f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,"
            "format=rgb24",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-",
        ],
        check=True,
        capture_output=True,
    ).stdout
    frame_size = width * height * 3
    if len(decoded) % frame_size:
        raise RuntimeError(f"FFmpeg returned a partial RGB frame for {source}.")
    frames = [
        Image.frombytes("RGB", (width, height), decoded[offset : offset + frame_size])
        for offset in range(0, len(decoded), frame_size)
    ]
    if len(frames) < 3:
        raise RuntimeError(f"Expected at least 3 decoded frames in {source}.")
    return frames, width, height


def create_forward_loop(
    ffmpeg: str,
    source: Path,
    destination: Path,
    seconds: int,
    cycles: int,
    slowdown: float,
) -> None:
    if seconds <= 0 or cycles <= 0 or slowdown <= 1:
        raise SystemExit("--seconds and --cycles must be positive; --slowdown must exceed 1.")
    if not source.is_file():
        raise SystemExit(f"Source animation was not found: {source}")
    if destination.exists():
        raise SystemExit(f"Refusing to overwrite existing output: {destination}")

    total_frames = seconds * FPS
    if total_frames % cycles:
        raise SystemExit(
            f"{seconds} seconds at {FPS} fps must contain a frame count divisible "
            f"by --cycles ({cycles})."
        )
    period_frames = total_frames // cycles
    frames, width, height = decode_frames(ffmpeg, source, slowdown)
    overlap_frames = len(frames) - period_frames
    if overlap_frames < 2:
        raise SystemExit(
            f"The requested loop leaves only {overlap_frames} crossfade frames. "
            "Use fewer cycles or a shorter duration."
        )
    if overlap_frames >= len(frames):
        raise SystemExit(
            "The requested loop period is too short for this source animation."
        )

    cycle = [
        Image.blend(
            frames[period_frames + index],
            frames[index],
            index / (overlap_frames - 1),
        )
        for index in range(overlap_frames)
    ]
    cycle.extend(frames[overlap_frames:period_frames])
    if len(cycle) != period_frames:
        raise RuntimeError(
            f"Loop construction produced {len(cycle)} frames; expected {period_frames}."
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{width}x{height}",
        "-r",
        str(FPS),
        "-i",
        "pipe:0",
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(destination),
    ]
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.stdin is None or process.stderr is None:
        raise RuntimeError("Could not open FFmpeg input/output pipes.")
    try:
        for _ in range(cycles):
            for frame in cycle:
                process.stdin.write(frame.tobytes())
    except BrokenPipeError as error:
        process.stdin.close()
        message = process.stderr.read().decode("utf-8", "replace")
        process.wait()
        raise RuntimeError(f"FFmpeg stopped while encoding the loop: {message}") from error
    else:
        process.stdin.close()
        message = process.stderr.read().decode("utf-8", "replace")
        status = process.wait()
        if status:
            raise RuntimeError(f"FFmpeg failed to encode the loop: {message}")

    print(
        f"Saved {destination} ({seconds}s, {total_frames} frames, "
        f"{overlap_frames} crossfade frames per cycle, "
        f"{width}x{height}, slowdown {slowdown:g}x)."
    )


def main() -> None:
    args = parse_args()
    source = args.input.expanduser().resolve()
    destination = (
        args.output.expanduser().resolve()
        if args.output
        else source.with_name(f"{source.stem}-forward-loop.mp4")
    )
    create_forward_loop(
        resolve_ffmpeg(args.ffmpeg),
        source,
        destination,
        args.seconds,
        args.cycles,
        args.slowdown,
    )


if __name__ == "__main__":
    main()
