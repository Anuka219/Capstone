# AGENTS.md — Project rules & context (READ THIS FIRST)

**Single source of truth for the MEM/MIM Guide Bot.** Two AI coding assistants
work on this repo and do NOT share memory. Read this file before editing, and
**update it whenever a decision changes**. (Claude Code reads `CLAUDE.md`, which
just points here.)

## What this is
A chatbot answering prospective & enrolled students' questions about two
Hochschule Pforzheim master's programs: **MEM** (Engineering and Management) and
**MIM** (Industrial Management). Student capstone. **Presentation: 24 June 2026.**

## Run it
```
cd Capstone/Capstone
source ../.venv/bin/activate
uvicorn app:app --host 127.0.0.1 --port 8000
# open http://localhost:8000/
```
Restart after editing `app.py`, `.env`, or `knowledge_docs/`
(`kill $(lsof -ti :8000)` first). `index.html` and `LOGO.png` are served fresh —
just hard-refresh the browser, no restart needed.

## Architecture
- `app.py` — FastAPI backend (the real app): SYSTEM_PROMPT, LLM calls, voice,
  knowledge retrieval, timetable + calendar.
- `index.html` — single-page frontend served at `/`.
- `knowledge_docs/` — facts retrieved into answers: `MEM_MIM_curated_facts.md`
  (facts), `Semesteruebersicht_SS26.md` (general SS26 timetable), and
  `MIM_English_Track_Timetable_SS26.md` (room-aware MIM English Track / Varsha
  timetable extracted from the provided PDF). `Course_Professors_SS26.md` maps
  course names to professor / instructor names for direct "course prof" answers.
- `bot_memory/` — learned corrections + per-session conversation memory.
- `LOGO.png` — HS Pforzheim logo, served via `GET /LOGO.png`.
- `.env` — secrets (NOT committed). `.env.example` lists the keys.

## LLM
- **Groq `llama-3.1-8b-instant`** is the only active model. Free tier =
  6,000 tokens/MINUTE — the real bottleneck. Keep the SYSTEM_PROMPT lean.
- **OpenRouter is DISABLED** (`OPENROUTER_ENABLED=false`) — dead key. Don't re-enable.
- **Gemini fallback is wired but OFF** — user's keys return 0 quota (EEA needs
  Google billing). Code ready in `configured_ai_providers()`; uncomment
  `GEMINI_API_KEY` in `.env` only with a funded key.
- Conversation memory: per-session, in `bot_memory/conversation_history.json`.

## Voice
ElevenLabs, **English only** (`eleven_turbo_v2_5` + `language_code=en` so the
cloned voice can't drift into German). VOICE_ID `EV4DOTEgIuaWXU5Z948S`. On-click.

## LOCKED DECISIONS — do NOT undo these
1. **Never invent facts.** No made-up fees, numbers, dates, scores, or steps.
   There is **NO application fee** for the online portal. If unknown → say
   "I don't have that information."
2. **MIM English Track = fully English, NO German certificate** for admission
   (only English, e.g. TOEFL/IELTS). German requirement is **C1 (not C2)**, and
   only for German-taught programs AND only for non-native German speakers;
   native speakers / a German-taught prior degree are exempt. For language
   requirement questions, define the requirements directly; do **not** append
   "For more information..." or links to the application/language pages.
3. **Tuition:** non-EU/EEA = **€1,500/semester**; EU/EEA & German-Abitur holders
   pay none; everyone pays a ~€150–170 semester contribution.
4. **Schedules: the chat ANSWERS** timetable/class/exam questions from the SS26
   timetable (`direct_timetable_answer()`). The user chose this — do NOT switch
   it back to "redirect to the calendar." Application/admission deadlines are
   separate → answer with real dates (15 Jan summer / 15 June winter).
   "My schedule", "my timetable", "what do I have", "where should I go", and
   similar personal schedule questions default to **MIM E-Track** / the Varsha
   timetable. Schedule answers must include date/day, time, block, class,
   audience, and room when the timetable provides it.
5. **Answer style:** short, scannable, spoken-first (first 2–4 sentences must
   stand alone for the voice; tables are not read aloud).
6. **Course professor questions:** answer from `Course_Professors_SS26.md` /
   visible timetable `Lehrperson` data. If a course is not listed, say "I don't
   have the professor information for that course." Do not guess.
7. **Groq-only** for the demo; **voice English-only**.

## Coordinating two AIs (important)
- **Always re-read a file before editing** — it may have changed since your last
  turn (the other assistant may have edited it).
- **Don't overwrite the other assistant's work.** If code looks unfamiliar, it
  may be theirs — preserve it, don't delete it.
- **Commit after a working session** so changes are visible and recoverable
  (almost nothing was tracked before — see git log).
- **Update this file** whenever a new decision is made or a locked one changes.
