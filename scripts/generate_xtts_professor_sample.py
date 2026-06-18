#!/usr/bin/env python3
"""
Generate a professor-style voice sample with Coqui XTTS-v2.

This uses a short reference clip and writes the result where app.py can serve it
through the chatbot speaker button:

    voice_source/generated/professor_voice_sample.wav

Install first:
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install TTS
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path


DEFAULT_TEXT = (
    "Hello, I am the MEM and MIM Guide Bot. I can help you compare both programs "
    "and understand the application process."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a local XTTS-v2 professor voice sample.")
    parser.add_argument("--text", default=DEFAULT_TEXT, help="English text to synthesize.")
    parser.add_argument(
        "--speaker",
        default="voice_source/instant_voice_clone_clips/raphael_10s_45min.mp3",
        help="Reference speaker audio clip.",
    )
    parser.add_argument(
        "--output",
        default="voice_source/generated/professor_voice_sample.wav",
        help="Output WAV file.",
    )
    parser.add_argument("--language", default="en", help="XTTS language code, for example en or de.")
    parser.add_argument("--gpu", action="store_true", help="Use GPU if available.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent.parent
    speaker = root / args.speaker
    output = root / args.output

    if not speaker.exists():
        raise SystemExit(f"Speaker reference clip not found: {speaker}")

    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        from TTS.api import TTS
    except ImportError as exc:
        raise SystemExit(
            "Missing Coqui TTS. Install it first:\n"
            "  cd /Users/anukavarsha/Downloads/Capstone/Capstone\n"
            "  python3 -m venv .venv\n"
            "  source .venv/bin/activate\n"
            "  python -m pip install TTS\n"
        ) from exc

    # Coqui asks for license/model consent on first run in some environments.
    os.environ.setdefault("COQUI_TOS_AGREED", "1")

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=args.gpu)
    tts.tts_to_file(
        text=args.text,
        speaker_wav=str(speaker),
        language=args.language,
        file_path=str(output),
    )
    print(f"Generated XTTS audio: {output}")


if __name__ == "__main__":
    main()
