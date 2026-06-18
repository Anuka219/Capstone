# Voice Extraction Guide for Raphael Voice Source

## Purpose

Raphael suggested using the videos from the HS Pforzheim video portal as the largest source of his voice. The reachable portal URL is `https://video.hs-pforzheim.de`. For the capstone, the goal is to download suitable MP4 videos, extract the speech audio, clean it if needed, and use the approved voice material for the chatbot voice demo.

Important: use this voice material only for the agreed project purpose and mention in the presentation/report that the source was provided by Raphael.

## Recommended Workflow

1. Open `https://video.hs-pforzheim.de` in the browser.
2. Search for videos where Raphael is speaking clearly.
3. Download the MP4 files from the video page if the portal provides a download button.
4. Put the downloaded files into a folder such as:

```text
Capstone/voice_source/videos/
```

5. Extract the audio from each MP4.
6. Convert the audio to a clean WAV file.
7. Listen and remove sections with music, silence, other speakers, or background noise.
8. Use only clear speech samples for the voice feature.

## Option A: Extract Audio With macOS avconvert

This Mac already has `avconvert`, so you can extract `.m4a` audio without installing FFmpeg.

After placing MP4 files inside `Capstone/voice_source/videos/`, run:

```bash
cd /Users/anukavarsha/Downloads/Capstone/Capstone
zsh scripts/extract_prof_voice_audio_macos.sh
```

The audio files will be created in:

```text
Capstone/voice_source/audio/
```

## Option B: Install FFmpeg

FFmpeg is the easiest tool for extracting audio from videos.

If Homebrew is available:

```bash
brew install ffmpeg
```

If Homebrew is not available, download FFmpeg for macOS from:

```text
https://ffmpeg.org/download.html
```

After installation, check:

```bash
ffmpeg -version
```

## Extract Audio From One MP4

Use this command after placing a video inside `Capstone/voice_source/videos/`:

```bash
ffmpeg -i "voice_source/videos/input_video.mp4" -vn -ac 1 -ar 44100 "voice_source/audio/raphael_01.wav"
```

Meaning:

- `-i` selects the input video.
- `-vn` removes the video stream.
- `-ac 1` converts the audio to mono.
- `-ar 44100` sets the sample rate to 44.1 kHz.
- The output is a WAV audio file.

## Extract Audio From Multiple MP4 Files

Create the output folder first:

```bash
mkdir -p voice_source/audio
```

Then run this from inside the `Capstone` project folder:

```bash
for f in voice_source/videos/*.mp4; do
  name=$(basename "$f" .mp4)
  ffmpeg -i "$f" -vn -ac 1 -ar 44100 "voice_source/audio/${name}.wav"
done
```

## Optional Audio Cleaning

If the extracted audio has background noise, use Audacity:

1. Open the WAV file in Audacity.
2. Remove long silences, music, audience noise, or other speakers.
3. Keep only clear sections where Raphael is speaking.
4. Export again as WAV.

Recommended voice sample quality:

- Clear speech.
- Minimal background noise.
- One speaker only.
- Several short clips are better than one very long noisy file.
- Around 5 to 20 minutes of clean speech is useful for a demo voice workflow, depending on the voice tool requirements.

## How To Mention This In The Report

Add this sentence to the implementation or tools section:

```text
For the voice feature, Raphael provided permission to use his publicly available HS Pforzheim video recordings as a voice source. We planned to download the MP4 files, extract the audio channel, and use clean speech samples for the chatbot voice demo.
```

## Presentation Slide Idea

Slide title: Voice Feature

Bullet points:

- Voice source suggested by Raphael.
- MP4 videos collected from HS Pforzheim video portal.
- Audio extracted from video files.
- Clean speech samples prepared for text-to-speech or voice cloning workflow.
- Used only for the educational capstone demo with permission.
