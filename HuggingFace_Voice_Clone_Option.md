# Hugging Face Voice Clone Option

## Which Tool Can Do What?

- **Hugging Face:** yes, possible. Public Spaces such as XTTS-v2 or OpenVoice can clone from a reference audio clip if the Space is running and accepts uploads.
- **OpenRouter:** no, not for voice cloning. OpenRouter is useful for the chatbot text answer, not professor-style audio generation.
- **NotebookLM:** no, not for this. NotebookLM can create audio-style summaries, but it does not provide a custom professor voice ID or chatbot TTS voice clone.

## Recommended Route

Use Hugging Face with a voice-cloning Space:

- `coqui/XTTS-v2` model page: `https://huggingface.co/coqui/XTTS-v2`
- OpenVoice Space option: `https://huggingface.co/spaces/myshell-ai/OpenVoiceV2`

XTTS-v2 supports voice cloning from a short reference clip and can generate English speech from a German reference voice.

## Prepared Reference Clips

Use one of these clips as the speaker/reference file:

```text
voice_source/elevenlabs_clips/raphael_clip_45min.mp3
voice_source/elevenlabs_clips/raphael_clip_55min.mp3
voice_source/elevenlabs_clips/raphael_clip_75min.mp3
```

Pick the cleanest clip where Raphael is speaking alone.

## Option A: Use Hugging Face In Browser

1. Open a voice-cloning Space, for example OpenVoiceV2.
2. Upload one clean Raphael reference clip.
3. Enter English text for the chatbot sample.
4. Generate audio.
5. Download the generated audio.
6. Put the generated audio into:

```text
voice_source/generated/
```

This is the easiest path if the Space UI is working.

## Option B: Use Hugging Face From Script

Install the Gradio client:

```bash
python3 -m pip install gradio_client
```

Inspect the Space API:

```bash
cd /Users/anukavarsha/Downloads/Capstone/Capstone
python3 scripts/huggingface_voice_clone.py --space "myshell-ai/OpenVoiceV2" --view-api
```

The script will print the exact input order. Then call the Space using the correct `--api-name` and `--args`.

Because public Spaces change their API schemas, we must inspect `--view-api` first before making the final command.

## How It Connects To The Chatbot

There are two possible integration levels:

1. **Simple demo:** generate one or more professor-style audio samples in Hugging Face and play them during the presentation.
2. **Chatbot integration:** create a local endpoint that sends each bot response to Hugging Face and returns the generated audio.

For the capstone, the simple demo is safer because public Hugging Face Spaces may sleep, queue, or change their API.

