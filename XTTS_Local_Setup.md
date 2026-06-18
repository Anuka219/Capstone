# Local XTTS Voice Clone Setup

## Why XTTS?

XTTS-v2 can clone a voice from a short reference clip and generate speech in English. The Coqui model page says it supports voice cloning from a quick 6-second audio clip, cross-language voice cloning, multilingual generation, and English output.

## Reference Clip

Use this prepared 10-second clip:

```text
voice_source/instant_voice_clone_clips/raphael_10s_45min.mp3
```

## Install

From the project folder:

```bash
cd /Users/anukavarsha/Downloads/Capstone/Capstone
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install TTS
```

## Generate Professor-Style Audio

```bash
source .venv/bin/activate
python scripts/generate_xtts_professor_sample.py
```

The generated file will be:

```text
voice_source/generated/professor_voice_sample.wav
```

The chatbot backend automatically checks for this file and uses it for the speaker button before falling back to ElevenLabs/browser speech.

## Run Chatbot

```bash
source .venv/bin/activate
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Open:

```text
http://127.0.0.1:8000/
```

## Notes

- On an Intel Mac CPU, generation may be slow.
- The first run downloads the XTTS model files, so it can take time.
- The output will be a professor-style approximation, not a perfect clone.

