#!/usr/bin/env python3
"""Generate a local image-to-video animation with an existing WanGP install."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INSTALL = Path.home() / ".local/share/darkzone-roleplay/WanGP"
DEFAULT_IMAGE = ROOT / "resources/imgs/characters/brunilda_1.jpeg"
FPS = 16
MAX_SINGLE_WINDOW_FRAMES = 257
GIF_WIDTH = 240
GIF_FPS = 8
GIF_COLORS = 64
PROMPT = (
    "Animate this still portrait as a calm, visibly living loop. Preserve Brunilda's "
    "identity, face, head, hands, pose, crown, clothing design, colors, painterly "
    "style, lighting, framing and background. Lock the camera. The cloak is the "
    "main moving part: its loose lower and side edges sway clearly but gently from "
    "side to side in a steady breeze, lifting and settling in a slow repeating "
    "rhythm. A few loose hair strands follow the breeze. Show a small, natural rise "
    "and fall of her shoulders and upper chest from breathing. Keep the torso, arms, "
    "hands and face otherwise still. Use a smooth cyclic motion and return close to "
    "the starting pose by the end. No walking, turning, speaking, facial expression "
    "changes, new objects, transformation, scene change, camera movement or zoom."
)
NEGATIVE_PROMPT = (
    "camera movement, zoom, pan, head turn, face change, identity change, flicker, "
    "warping, distortion, extra limbs, out of frame, scene change, new objects"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seconds",
        type=float,
        default=16,
        help="Requested duration in seconds (default: 16; maximum single window: 16).",
    )
    parser.add_argument(
        "--image",
        type=Path,
        default=DEFAULT_IMAGE,
        help="Starting image (default: Brunilda's portrait).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Source MP4 destination (defaults to output/video/ai/<image>-<seconds>s.mp4).",
    )
    parser.add_argument(
        "--wan2gp-dir",
        type=Path,
        default=Path(os.environ.get("WAN2GP_DIR", DEFAULT_INSTALL)),
        help=f"WanGP installation directory (default: {DEFAULT_INSTALL}).",
    )
    parser.add_argument(
        "--python",
        type=Path,
        help="Python executable for WanGP (defaults to <wan2gp-dir>/env_uv/bin/python).",
    )
    parser.add_argument("--prompt", default=PROMPT, help="Motion prompt.")
    parser.add_argument(
        "--negative-prompt",
        default=NEGATIVE_PROMPT,
        help="Content to avoid in the generated clip.",
    )
    parser.add_argument("--seed", type=int, default=56123, help="Generation seed.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate settings without loading the model or rendering.",
    )
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Create a seamless ping-pong loop MP4 from the generated clip.",
    )
    parser.add_argument(
        "--gif",
        action="store_true",
        help="Also export the loop as an optimized, infinitely looping GIF.",
    )
    parser.add_argument("--ffmpeg", help="FFmpeg executable for loop/GIF post-processing.")
    parser.add_argument(
        "--lora",
        type=str,
        help="LoRA adapter name to use (e.g., brunilda_lora_v1). Located in training/models/loras/",
    )
    return parser.parse_args()


def resolve_ffmpeg(requested: str | None, install: Path) -> str:
    if requested:
        return requested
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return ffmpeg
    bundled_ffmpeg = install / "ffmpeg_bins/ffmpeg"
    if bundled_ffmpeg.is_file():
        return str(bundled_ffmpeg)
    raise SystemExit(
        "FFmpeg was not found. Install FFmpeg or pass --ffmpeg /path/to/ffmpeg."
    )


def ffmpeg_environment(ffmpeg: str) -> dict[str, str] | None:
    executable = shutil.which(ffmpeg) or ffmpeg
    library_dir = Path(executable).expanduser().resolve().parent
    if not any(library_dir.glob("libavcodec.so*")):
        return None

    environment = os.environ.copy()
    library_path = environment.get("LD_LIBRARY_PATH")
    environment["LD_LIBRARY_PATH"] = os.pathsep.join(
        path for path in (str(library_dir), library_path) if path
    )
    return environment


def create_loop(
    ffmpeg: str,
    source: Path,
    destination: Path,
    frame_count: int,
    environment: dict[str, str] | None,
) -> None:
    reverse_end = frame_count - 1
    filter_complex = (
        f"[0:v]split=2[forward][reverse];"
        f"[reverse]reverse,trim=start_frame=1:end_frame={reverse_end},"
        f"setpts=PTS-STARTPTS[backward];"
        f"[forward]setpts=PTS-STARTPTS[front];"
        f"[front][backward]concat=n=2:v=1:a=0,fps={FPS},setsar=1[loop]"
    )
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-y",
            "-i",
            str(source),
            "-filter_complex",
            filter_complex,
            "-map",
            "[loop]",
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
        ],
        check=True,
        env=environment,
    )


def create_gif(
    ffmpeg: str,
    source: Path,
    destination: Path,
    environment: dict[str, str] | None,
) -> None:
    filter_complex = (
        f"[0:v]fps={GIF_FPS},scale={GIF_WIDTH}:-1:flags=lanczos,split[gif][palette];"
        f"[palette]palettegen=max_colors={GIF_COLORS}:stats_mode=diff[colors];"
        "[gif][colors]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle[output]"
    )
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-y",
            "-i",
            str(source),
            "-filter_complex",
            filter_complex,
            "-map",
            "[output]",
            "-loop",
            "0",
            str(destination),
        ],
        check=True,
        env=environment,
    )


def main() -> None:
    args = parse_args()
    if args.seconds <= 0:
        raise SystemExit("--seconds must be greater than zero.")

    install = args.wan2gp_dir.expanduser().resolve()
    python = (
        args.python.expanduser().absolute()
        if args.python
        else install / "env_uv/bin/python"
    )
    wgp = install / "wgp.py"
    image = args.image.expanduser().resolve()
    if not wgp.is_file():
        raise SystemExit(f"WanGP was not found at {wgp}. See resources/video/ai/README.md.")
    if not python.is_file():
        raise SystemExit(f"WanGP Python was not found at {python}.")
    if not image.is_file():
        raise SystemExit(f"Starting image was not found: {image}")

    frame_count = round(args.seconds * FPS) + 1
    if frame_count > MAX_SINGLE_WINDOW_FRAMES:
        maximum_seconds = (MAX_SINGLE_WINDOW_FRAMES - 1) / FPS
        raise SystemExit(
            f"This model supports up to {MAX_SINGLE_WINDOW_FRAMES} frames "
            f"({maximum_seconds:g} seconds) in a single window. Reduce --seconds "
            "to avoid concatenating separate generations."
        )
    settings = {
        "model_type": "i2v_nvfp4",
        "prompt": args.prompt,
        "negative_prompt": args.negative_prompt,
        "resolution": "480x832",
        "seed": args.seed,
        "image_start": str(image),
        "video_length": frame_count,
        "sliding_window_size": frame_count,
        "sliding_window_overlap": 1,
    }
    
    # Aggiungi LoRA se specificato
    if args.lora:
        lora_path = ROOT / "training/models/loras" / args.lora
        if not lora_path.is_dir():
            raise SystemExit(f"LoRA not found: {lora_path}")
        settings["custom_settings"] = {
            "lora_adapter": str(lora_path),
            "lora_scale": 1.0
        }
        print(f"✅ LoRA loaded: {args.lora}")
    
    loop_requested = args.loop or args.gif
    ffmpeg = (
        resolve_ffmpeg(args.ffmpeg, install)
        if loop_requested and not args.dry_run
        else None
    )
    ffmpeg_env = ffmpeg_environment(ffmpeg) if ffmpeg else None
    if args.output:
        destination = args.output.expanduser().resolve()
    else:
        destination = (
            ROOT
            / "output/video/ai"
            / f"{image.stem}-animazione-{args.seconds:g}s.mp4"
        )

    with tempfile.TemporaryDirectory(prefix="skarheim-wan2gp-") as temporary:
        run_dir = Path(temporary)
        settings_path = run_dir / "settings.json"
        output_dir = run_dir / "out"
        settings_path.write_text(json.dumps(settings, indent=2), encoding="utf-8")
        command = [str(python), str(wgp), "--process", str(settings_path)]
        if args.dry_run:
            command.append("--dry-run")
        else:
            output_dir.mkdir()
            command.extend(["--output-dir", str(output_dir)])

        print(
            f"Richiesti {frame_count} fotogrammi a {FPS} fps "
            f"(circa {frame_count / FPS:.1f} secondi)."
        )
        subprocess.run(command, cwd=install, check=True)
        if args.dry_run:
            return

        results = list(output_dir.glob("*.mp4"))
        if not results:
            raise SystemExit(f"WanGP finished without creating an MP4 in {output_dir}.")
        result = max(results, key=lambda path: path.stat().st_mtime_ns)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(result, destination)

    print(f"Video salvato in: {destination}")
    if loop_requested:
        if ffmpeg is None:
            raise SystemExit("FFmpeg is required to create a loop or GIF.")
        loop_path = destination.with_name(f"{destination.stem}-loop.mp4")
        create_loop(ffmpeg, destination, loop_path, frame_count, ffmpeg_env)
        print(f"Loop MP4 salvato in: {loop_path}")
        if args.gif:
            gif_path = destination.with_name(f"{destination.stem}-loop.gif")
            create_gif(ffmpeg, loop_path, gif_path, ffmpeg_env)
            print(f"GIF salvata in: {gif_path}")


if __name__ == "__main__":
    main()
