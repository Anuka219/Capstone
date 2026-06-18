#!/usr/bin/env python3
"""
Generate a professor-style speech sample through a Hugging Face Gradio Space.

This is intentionally configurable because public Spaces change their API names
and inputs. Run with --view-api first, then fill the matching arguments.

Example:
    python scripts/huggingface_voice_clone.py \
      --space "myshell-ai/OpenVoiceV2" \
      --view-api
"""

from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_TEXT = (
    "Hello, I am the MEM and MIM Guide Bot. I can help you compare the programs, "
    "understand application requirements, and prepare your next steps."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Call a Hugging Face voice-cloning Space.")
    parser.add_argument("--space", required=True, help="Hugging Face Space name, for example user/space-name.")
    parser.add_argument("--view-api", action="store_true", help="Print the Space API schema and exit.")
    parser.add_argument("--api-name", help="API endpoint name shown by view_api, such as /predict.")
    parser.add_argument("--text", default=DEFAULT_TEXT, help="Text to synthesize.")
    parser.add_argument(
        "--speaker",
        default="voice_source/elevenlabs_clips/raphael_clip_45min.mp3",
        help="Reference speaker audio clip.",
    )
    parser.add_argument(
        "--output",
        default="voice_source/generated/professor_voice_sample.wav",
        help="Where to save the generated audio if the Space returns a file.",
    )
    parser.add_argument(
        "--args",
        nargs="*",
        default=[],
        help=(
            "Extra positional arguments for the Space, in order. Use {text} and "
            "{speaker} placeholders if needed."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        from gradio_client import Client, handle_file
    except ImportError as exc:
        raise SystemExit(
            "Missing gradio_client. Install it first:\n"
            "  python3 -m pip install gradio_client\n"
        ) from exc

    client = Client(args.space)

    if args.view_api:
        client.view_api()
        return

    if not args.api_name:
        raise SystemExit("Pass --api-name after checking the Space with --view-api.")

    speaker_path = Path(args.speaker)
    if not speaker_path.exists():
        raise SystemExit(f"Speaker clip not found: {speaker_path}")

    call_args = []
    for value in args.args:
        if value == "{text}":
            call_args.append(args.text)
        elif value == "{speaker}":
            call_args.append(handle_file(str(speaker_path)))
        else:
            call_args.append(value)

    result = client.predict(*call_args, api_name=args.api_name)
    print("Space result:", result)

    if isinstance(result, str) and Path(result).exists():
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(Path(result).read_bytes())
        print(f"Saved generated audio to {output}")


if __name__ == "__main__":
    main()
