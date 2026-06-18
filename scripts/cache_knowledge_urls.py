#!/usr/bin/env python3
"""
Cache official web pages into knowledge_docs/web_cache.

Use this for official MEM/MIM pages, timetable pages, contact pages, module
pages, and FAQ pages. The chatbot then reads the cached HTML locally through
the existing knowledge_docs retrieval layer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent.parent
URL_FILE = ROOT / "knowledge_docs/source_urls.txt"
CACHE_DIR = ROOT / "knowledge_docs/web_cache"
USER_AGENT = "MEM-MIM-Guide-Bot-Capstone/1.0"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cache official web pages for chatbot knowledge.")
    parser.add_argument("--url-file", default=str(URL_FILE), help="Text file with one URL per line.")
    parser.add_argument("--output-dir", default=str(CACHE_DIR), help="Folder where cached HTML is stored.")
    parser.add_argument("--force", action="store_true", help="Re-download pages even when cached.")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between downloads in seconds.")
    return parser.parse_args()


def read_urls(path: Path) -> list[str]:
    if not path.exists():
        raise SystemExit(f"URL file not found: {path}")

    urls = []
    for line in path.read_text(encoding="utf-8").splitlines():
        clean = line.strip()
        if not clean or clean.startswith("#"):
            continue
        urls.append(clean)
    return urls


def safe_filename(url: str) -> str:
    parsed = urlparse(url)
    host = re.sub(r"[^a-zA-Z0-9]+", "-", parsed.netloc).strip("-")
    path = re.sub(r"[^a-zA-Z0-9]+", "-", parsed.path).strip("-") or "index"
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
    suffix = Path(parsed.path).suffix.lower()
    if suffix not in {".html", ".htm", ".pdf", ".txt", ".md", ".docx"}:
        suffix = ".html"
    if path.lower().endswith(suffix.lstrip(".")):
        path = path[: -(len(suffix) - 1)].rstrip("-") or "index"
    return f"{host}_{path}_{digest}{suffix}"


def fetch_url(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return response.read()


def write_metadata(path: Path, url: str) -> None:
    metadata_path = path.with_suffix(".json")
    metadata = {
        "source_url": url,
        "cached_at": datetime.now(timezone.utc).isoformat(),
        "cached_file": path.name,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()
    url_file = Path(args.url_file)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    urls = read_urls(url_file)
    if not urls:
        raise SystemExit(f"No URLs found in {url_file}. Add official pages first.")

    for index, url in enumerate(urls, 1):
        output = output_dir / safe_filename(url)
        if output.exists() and not args.force:
            print(f"[{index}/{len(urls)}] cached already: {output.relative_to(ROOT)}")
            continue

        print(f"[{index}/{len(urls)}] downloading: {url}")
        try:
            content = fetch_url(url)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            print(f"  failed: {exc}")
            continue

        output.write_bytes(content)
        write_metadata(output, url)
        print(f"  saved: {output.relative_to(ROOT)}")
        time.sleep(args.delay)

    print("\nDone. Reload chatbot knowledge with:")
    print("  curl -X POST http://127.0.0.1:8000/api/reload-knowledge")


if __name__ == "__main__":
    main()
