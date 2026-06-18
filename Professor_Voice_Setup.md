# Professor Voice Setup

## Current Status

The chatbot already supports voice output through ElevenLabs. The backend reads the voice from:

```text
ELEVENLABS_VOICE_ID
```

So after we create the professor voice in ElevenLabs, we only need to put that voice ID into `.env` and restart the bot.

If ElevenLabs asks for payment before creating a cloned professor voice, the project can still continue. The chatbot will use a placeholder/default voice or browser speech fallback, and the presentation can explain that the professor voice source audio was prepared but the final cloned voice ID required a paid ElevenLabs plan.

## Step 1: Download Voice Source Videos

Raphael suggested using his videos from:

```text
https://videos.hs-pforzheim.de
```

Download MP4 videos where Raphael is speaking clearly and place them here:

```text
Capstone/voice_source/videos/
```

Use only videos that are appropriate for the agreed capstone demo.

## Step 2: Extract WAV Audio

Install `ffmpeg` if it is not already installed. Then run this from the `Capstone` folder:

```bash
zsh scripts/extract_prof_voice_audio.sh
```

The extracted audio files will be created here:

```text
Capstone/voice_source/audio/
```

## Step 3: Clean The Audio

Before uploading to a voice tool, listen to the WAV files and remove:

- Long silence
- Music
- Other speakers
- Audience noise
- Sections with poor sound quality

Audacity is a good free tool for this. Export clean clips as WAV or MP3.

## Step 4: Create The ElevenLabs Voice

In ElevenLabs:

1. Go to the Voices section.
2. Create a new voice or instant voice clone.
3. Upload the clean Raphael speech samples.
4. Confirm the consent/permission requirement.
5. Save the voice.
6. Copy the generated `voice_id`.

## Step 5: Configure The Chatbot

Copy the environment template:

```bash
cp .env.example .env
```

Fill in:

```text
GROQ_API_KEY=...
```

OpenRouter can be used instead of Groq if preferred.

The chatbot is currently configured to use local XTTS first:

```text
VOICE_PROVIDER=xtts
XTTS_SPEAKER_WAV=voice_source/instant_voice_clone_clips/raphael_10s_45min.mp3
XTTS_LANGUAGE=en
```

These values are optional because `app.py` already has the same defaults.

## Step 6: Run The Bot

From the `Capstone` folder:

```bash
python3 -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Then open:

```text
http://127.0.0.1:8000/
```

Ask a question. The bot response should include a speaker button. Click it to hear the local XTTS professor-style voice.

The first spoken answer can take longer because XTTS loads the model. After that, repeated answers are cached in:

```text
Capstone/voice_source/generated/chat_responses/
```

To quickly confirm the backend voice mode:

```bash
curl http://127.0.0.1:8000/health
```

Look for:

```text
"voice_provider":"xtts"
"xtts_reference_clip":"...raphael_10s_45min.mp3"
```

When you send a real chat message, the API response should include:

```text
"voice_id":"local-xtts-professor-reference"
```

## Important Notes

- The page now uses the local backend by default when served from FastAPI.
- The professor-style voice is controlled by the local XTTS reference clip.
- ElevenLabs is no longer required for the demo voice.
- If XTTS audio is not available, the backend falls back to the saved sample, then ElevenLabs if configured, then browser speech synthesis.
- Use the voice only for the educational capstone demo and with the permission Raphael provided.
- If audio fails, check the server terminal for XTTS errors.

## Presentation Wording If Voice Cloning Is Paid

Use this wording:

```text
We prepared the professor voice workflow by downloading Raphael's approved HS Pforzheim video, extracting the audio, and creating clean reference clips. ElevenLabs professional cloning required a paid plan, so we used local XTTS instead. The chatbot generates spoken responses with a professor-style reference voice for the educational capstone demo.
```
