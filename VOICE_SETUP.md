# Professor Voice Setup (Local XTTS Cloning)

The chatbot clones the professor's voice **locally and for free** using Coqui
XTTS v2. Each answer is spoken in the professor's voice and cached, so the
second time an answer is played it is instant.

## How it works

- `VOICE_PROVIDER=xtts` in `.env` turns on local voice cloning.
- The reference clip is `XTTS_SPEAKER_WAV` (currently
  `voice_source/instant_voice_clone_clips/raphael_10s_65min.mp3`).
- When you click the speaker button, the backend generates a WAV in the
  professor's voice for that exact answer and caches it in
  `voice_source/generated/chat_responses/`.
- First generation per unique answer takes ~30s on CPU. After that it is
  instant (served from cache).

## One-time install (Python 3.9)

The default `pip install TTS` fails on Python 3.9 because of several
dependencies that dropped 3.9 support. These exact pins work:

```bash
source ../.venv/bin/activate        # the project venv at Capstone/.venv
python -m pip install --upgrade pip  # old pip 21.x has very slow resolution
python -m pip install "spacy==3.7.5" "thinc<8.3.0" "TTS==0.22.0"
python -m pip install "setuptools<81"        # librosa still needs pkg_resources
python -m pip install "bangla==0.0.2"        # 0.0.5 uses py3.10+ syntax
python -m pip install "transformers==4.40.2" # newer ones removed BeamSearchScorer
```

Or simply: `pip install -r requirements.txt` (the frozen working set).

## Run the server

```bash
cd Capstone/Capstone
source ../.venv/bin/activate
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Then open http://127.0.0.1:8000/ .

IMPORTANT: if voice ever seems "stuck" on robotic browser speech, an **old
server process** is probably still running on port 8000 with stale settings.
Kill it first:

```bash
kill $(lsof -ti :8000)
```

## Optional: HuggingFace OpenVoice (hosted)

`VOICE_PROVIDER=openvoice_hf` uses the HuggingFace OpenVoice V2 Space instead,
with automatic fallback to local XTTS. As of June 2026 the public Spaces
(`myshell-ai/OpenVoiceV2`, `coqui/xtts`) were returning RUNTIME_ERROR, so local
`xtts` is the reliable choice for the demo. Switch back only if a Space is
confirmed working.
