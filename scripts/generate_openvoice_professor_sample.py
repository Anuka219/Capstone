#!/usr/bin/env python3
"""
Generate a professor-style voice sample with OpenVoiceV2 + MeloTTS.

This adapts the official OpenVoice demo_part3.ipynb flow:
1. Extract tone color from the professor reference clip.
2. Generate base English speech with MeloTTS.
3. Convert the base speech to the reference speaker tone color.

Expected setup:
    openvoice_workbench/OpenVoice/
    openvoice_workbench/OpenVoice/checkpoints_v2/

Output:
    voice_source/generated/openvoice_professor_sample.wav
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


DEFAULT_TEXT = (
    "Hello, I am the MEM and MIM Guide Bot. I can help you compare the programs "
    "and understand the application process."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an OpenVoiceV2 professor voice sample.")
    parser.add_argument("--text", default=DEFAULT_TEXT, help="English text to synthesize.")
    parser.add_argument(
        "--reference",
        default="voice_source/instant_voice_clone_clips/raphael_10s_45min.mp3",
        help="Reference speaker audio clip.",
    )
    parser.add_argument(
        "--openvoice-dir",
        default="openvoice_workbench/OpenVoice",
        help="Local OpenVoice repository folder.",
    )
    parser.add_argument(
        "--output",
        default="voice_source/generated/openvoice_professor_sample.wav",
        help="Final output WAV file.",
    )
    parser.add_argument("--language", default="EN_NEWEST", help="MeloTTS language, for example EN_NEWEST or EN.")
    parser.add_argument("--speed", type=float, default=1.0, help="MeloTTS speech speed.")
    return parser.parse_args()


def resolve(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent.parent
    openvoice_dir = resolve(root, args.openvoice_dir)
    reference = resolve(root, args.reference)
    output = resolve(root, args.output)
    checkpoint_dir = openvoice_dir / "checkpoints_v2"
    converter_dir = checkpoint_dir / "converter"

    if openvoice_dir.exists():
        sys.path.insert(0, str(openvoice_dir))

    if not reference.exists():
        raise SystemExit(f"Reference audio not found: {reference}")
    if not converter_dir.exists():
        raise SystemExit(
            "OpenVoiceV2 checkpoints not found. Expected folder:\n"
            f"  {converter_dir}\n"
            "Download and extract the official checkpoints_v2 first."
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    work_dir = output.parent / "openvoice_tmp"
    work_dir.mkdir(parents=True, exist_ok=True)
    src_path = work_dir / "melo_base.wav"

    import torch
    from melo.api import TTS
    from openvoice import se_extractor
    from openvoice.api import ToneColorConverter

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    if torch.backends.mps.is_available() and device == "cpu":
        torch.backends.mps.is_available = lambda: False

    tone_color_converter = ToneColorConverter(str(converter_dir / "config.json"), device=device)
    tone_color_converter.load_ckpt(str(converter_dir / "checkpoint.pth"))
    target_se, _audio_name = se_extractor.get_se(str(reference), tone_color_converter, vad=True)

    model = TTS(language=args.language, device=device)
    speaker_ids = model.hps.data.spk2id
    speaker_name = next(iter(speaker_ids.keys()))
    speaker_id = speaker_ids[speaker_name]
    speaker_key = speaker_name.lower().replace("_", "-")
    source_se_path = checkpoint_dir / "base_speakers/ses" / f"{speaker_key}.pth"

    if not source_se_path.exists():
        raise SystemExit(f"Base speaker embedding not found: {source_se_path}")

    source_se = torch.load(str(source_se_path), map_location=device)
    model.tts_to_file(args.text, speaker_id, str(src_path), speed=args.speed)

    tone_color_converter.convert(
        audio_src_path=str(src_path),
        src_se=source_se,
        tgt_se=target_se,
        output_path=str(output),
        message="@MyShell",
    )
    print(f"Generated OpenVoice audio: {output}")


if __name__ == "__main__":
    main()
