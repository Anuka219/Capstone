#!/bin/zsh
set -e

cd "$(dirname "$0")/.."

if ! command -v avconvert >/dev/null 2>&1; then
  echo "avconvert is required but was not found on this Mac."
  exit 1
fi

mkdir -p voice_source/audio

found=0
for file in voice_source/videos/*.mp4; do
  [ -e "$file" ] || continue
  found=1
  name="$(basename "$file" .mp4)"
  avconvert --source "$file" --preset PresetAppleM4A --output "voice_source/audio/${name}.m4a" --replace
done

if [ "$found" -eq 0 ]; then
  echo "No MP4 files found in voice_source/videos."
  echo "Download Raphael's MP4 videos there first, then rerun this script."
  exit 1
fi

echo "Done. Extracted M4A files are in voice_source/audio."
