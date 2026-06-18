#!/bin/zsh

cd "$(dirname "$0")"

if [ -d ".venv" ]; then
  source ".venv/bin/activate"
elif [ -d "venv" ]; then
  source "venv/bin/activate"
fi

python3 - <<'PY'
import importlib.util
import sys

missing = [
    package
    for package in ("fastapi", "uvicorn", "httpx", "dotenv")
    if importlib.util.find_spec(package) is None
]

if missing:
    print("Missing Python packages: " + ", ".join(missing))
    print()
    print("Run these commands once:")
    print("  cd /Users/anukavarsha/Downloads/Capstone/Capstone")
    print("  python3 -m venv .venv")
    print("  source .venv/bin/activate")
    print("  pip install -r requirements.txt")
    sys.exit(1)
PY

if [ $? -ne 0 ]; then
  echo
  echo "Press any key to close this window."
  read -k 1
  exit 1
fi

python3 -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload &
SERVER_PID=$!
sleep 2
open "http://127.0.0.1:8000/"
wait $SERVER_PID
