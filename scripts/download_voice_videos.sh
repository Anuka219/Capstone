#!/bin/zsh
set -e

cd "$(dirname "$0")/.."

URL_FILE="voice_source/video_urls.txt"
OUT_DIR="voice_source/videos"

mkdir -p "$OUT_DIR"

if [ ! -f "$URL_FILE" ]; then
  echo "Missing $URL_FILE"
  exit 1
fi

count=0
while IFS= read -r url; do
  url="${url#"${url%%[![:space:]]*}"}"
  url="${url%"${url##*[![:space:]]}"}"

  if [ -z "$url" ] || [[ "$url" == \#* ]]; then
    continue
  fi

  count=$((count + 1))
  output="$OUT_DIR/raphael_source_${count}.mp4"
  echo "Downloading $url"
  curl -L --fail --output "$output" "$url"
  echo "Saved $output"
done < "$URL_FILE"

if [ "$count" -eq 0 ]; then
  echo "No URLs found in $URL_FILE."
  echo "Paste one direct MP4/download URL per line, then run this script again."
  exit 1
fi

echo "Done. Downloaded $count video file(s) into $OUT_DIR."
