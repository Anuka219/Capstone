import json
import os
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HTML_FILE = ROOT / "MEM-Guide-Bot-Website.html"
AI_PROVIDER = os.getenv("AI_PROVIDER", "openrouter").lower()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

SYSTEM_PROMPT = """
You are the MEM & MIM Guide Bot for a student capstone demo.
Answer like a friendly, careful study advisor for Hochschule Pforzheim's
MEM Engineering and Management M.Sc. and MIM Industrial Management M.Sc.

Use this knowledge as your source:

MEM:
- MEM is Engineering and Management M.Sc.
- It is a technical-management master focused on leadership, production
  strategy, process management, market-oriented product development,
  strategic procurement, value-oriented management, emerging technologies,
  interdisciplinary research, capstone seminar, colloquium, and thesis.
- It is listed as a Master of Science, 3 semesters including thesis,
  90 ECTS, with English/German teaching.
- The English page lists 15 June for winter intake. The German engineering
  master overview also lists 15 January for summer and 15 June for winter.
- The German page mentions an industrial-engineering degree profile, grade
  2.5 or better, B2 English, and C1 German for non-native German speakers.

MIM:
- MIM is Industrial Management M.Sc.
- It is broader industrial management, connecting technology, business,
  leadership, processes, data, innovation, and company-wide problem solving.
- Official themes include Technology and Innovation Management, Leadership,
  Process and Data Management, and Networked Systems & Artificial Intelligence.
- It is listed as Master of Science, full-time, 3 semesters including thesis,
  90 ECTS, 24 places, summer and winter intake, German/English teaching,
  and admission through a selection procedure.

Application:
- Students apply through the HS Pforzheim online application portal.
- Documents may include CV, university entrance qualification proof,
  first-degree proof/transcript, motivation letter, recommendation,
  professional or educational proof, stays abroad, references, and language
  certificates depending on the program.

Rules:
- Be helpful, natural, and concise.
- Do not invent exact fees, deadlines, or admission guarantees.
- If a detail may change, tell the user to verify it on the official
  HS Pforzheim page or application portal.
- The bot can estimate fit, but HS Pforzheim makes the official decision.
- If the user asks unrelated questions, gently bring them back to MEM/MIM.
""".strip()


def json_response(handler, status, payload):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(body)


def extract_openai_text(response):
    if response.get("output_text"):
        return response["output_text"].strip()

    parts = []
    for item in response.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if text:
                parts.append(text)
    return "\n".join(parts).strip()


def extract_chat_text(response):
    choices = response.get("choices", [])
    if not choices:
        return ""
    message = choices[0].get("message", {})
    return str(message.get("content", "")).strip()


def ask_openai(question):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        "temperature": 0.4,
    }

    request = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=45) as result:
        data = json.loads(result.read().decode("utf-8"))

    answer = extract_chat_text(data)
    if not answer:
        raise RuntimeError("The AI response did not contain text.")
    return answer


def ask_openrouter(question):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set.")

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        "temperature": 0.4,
    }

    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "MEM MIM Guide Bot Capstone",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=45) as result:
        data = json.loads(result.read().decode("utf-8"))

    answer = extract_chat_text(data)
    if not answer:
        raise RuntimeError("The AI response did not contain text.")
    return answer


def ask_ai(question):
    if AI_PROVIDER == "openai":
        return ask_openai(question), OPENAI_MODEL
    if AI_PROVIDER == "openrouter":
        return ask_openrouter(question), OPENROUTER_MODEL
    raise RuntimeError("AI_PROVIDER must be 'openrouter' or 'openai'.")


class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        if self.path not in {"/", "/MEM-Guide-Bot-Website.html"}:
            self.send_error(404)
            return

        content = HTML_FILE.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            question = str(payload.get("message", "")).strip()
            if not question:
                json_response(self, 400, {"error": "Please send a message."})
                return
            reply, model = ask_ai(question)
            json_response(self, 200, {
                "text": reply,
                "model": model,
                "provider": AI_PROVIDER,
                "audio_base64": "",
                "audio_mime": "audio/mpeg",
            })
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            json_response(self, error.code, {"error": detail})
        except Exception as error:
            json_response(self, 500, {"error": str(error)})

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


def main():
    port = int(os.getenv("PORT", "8000"))
    server = ThreadingHTTPServer(("localhost", port), Handler)
    print(f"MEM/MIM AI server running at http://localhost:{port}")
    print(f"Using provider: {AI_PROVIDER}")
    print(f"OpenRouter model: {OPENROUTER_MODEL}")
    print(f"OpenAI model: {OPENAI_MODEL}")
    if AI_PROVIDER == "openrouter" and not os.getenv("OPENROUTER_API_KEY"):
        print("OPENROUTER_API_KEY is not set yet. Set it before asking AI questions.")
    if AI_PROVIDER == "openai" and not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set yet. Set it before asking AI questions.")
    server.serve_forever()


if __name__ == "__main__":
    main()
