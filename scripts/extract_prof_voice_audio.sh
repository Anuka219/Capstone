#!/bin/zsh
set -e

cd "$(dirname "$0")/.."

FFMPEG="ffmpeg"
if [ -x "tools/ffmpeg" ]; then
  FFMPEG="tools/ffmpeg"
fi

if ! command -v "$FFMPEG" >/dev/null 2>&1; then
  echo "ffmpeg is required but not installed."
  echo "Install ffmpeg first, then run this script again."
  exit 1
fi

mkdir -p voice_source/audio

found=0
for file in voice_source/videos/*.mp4; do
  [ -e "$file" ] || continue
  found=1
  name="$(basename "$file" .mp4)"
  "$FFMPEG" -y -i "$file" -vn -ac 1 -ar 44100 "voice_source/audio/${name}.wav"
  "$FFMPEG" -y -i "voice_source/audio/${name}.wav" -codec:a libmp3lame -b:a 128k "voice_source/audio/${name}.mp3"
done

if [ "$found" -eq 0 ]; then
  echo "No MP4 files found in voice_source/videos."
  echo "Download Raphael's MP4 videos there first, then rerun this script."
  exit 1
fi

echo "Done. Extracted WAV files are in voice_source/audio."
