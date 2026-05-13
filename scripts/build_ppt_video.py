from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = (
    ROOT
    / "outputs"
    / "manual-20260513-233428-recallguard"
    / "presentations"
    / "recallguard-foundry-submission"
)
PREVIEW = WORKSPACE / "preview"
FINAL = ROOT / "final"
ASSETS = FINAL / "ppt_video_assets"
SCRIPT = FINAL / "RecallGuard_AI_PPT_Video_Script_Somi.md"
OUTPUT = FINAL / "RecallGuard_AI_PPT_Demo_Somi.mp4"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def narrations() -> list[str]:
    text = SCRIPT.read_text(encoding="utf-8")
    blocks = []
    for section in re.split(r"\n## Slide \d+ .*?\n", text)[1:]:
        section = section.strip()
        if not section:
            continue
        blocks.append(" ".join(section.split()))
    if len(blocks) != 10:
        raise RuntimeError(f"Expected 10 narration blocks, got {len(blocks)}")
    return blocks


def audio_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    segments: list[Path] = []

    for index, narration in enumerate(narrations(), start=1):
        image = PREVIEW / f"slide-{index:02d}.png"
        audio = ASSETS / f"slide_{index:02d}.aiff"
        segment = ASSETS / f"segment_{index:02d}.mp4"
        if not image.exists():
            raise FileNotFoundError(image)

        run(["say", "-v", "Samantha", "-r", "178", "-o", str(audio), narration])
        duration = max(audio_duration(audio) + 0.7, 5.0)
        run(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-i",
                str(image),
                "-i",
                str(audio),
                "-t",
                f"{duration:.2f}",
                "-vf",
                "scale=1920:1080,format=yuv420p",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-tune",
                "stillimage",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                "-shortest",
                str(segment),
            ]
        )
        segments.append(segment)

    concat = ASSETS / "segments.txt"
    concat.write_text(
        "".join(f"file '{segment.as_posix()}'\n" for segment in segments),
        encoding="utf-8",
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-c",
            "copy",
            str(OUTPUT),
        ]
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
