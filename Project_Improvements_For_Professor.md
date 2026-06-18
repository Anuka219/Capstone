# Project Improvements For Professor Feedback

## 1. Faster Answers

Problem: The chatbot response was slow because `/api/chat` generated the text
answer and waited for XTTS voice synthesis before returning anything to the
browser.

Fix: Text and voice are now separated.

- `/api/chat` returns the answer quickly.
- `/api/voice` generates professor-style audio only when the speaker button is
  clicked.
- The first voice generation can still take time, but it no longer blocks the
  answer.

## 2. Document-Based Answers

The chatbot now has a local document retrieval layer.

- Put official PDFs, DOCX, TXT, Markdown, or HTML files in `knowledge_docs/`.
- At startup, the backend indexes these files into searchable chunks.
- For each user question, the most relevant excerpts are added to the AI prompt.
- This helps the bot answer more precisely from project documents instead of
  only relying on the hard-coded prompt.
- Official web pages can be cached locally using `scripts/cache_knowledge_urls.py`.
  This avoids slow and unreliable live scraping during the demo.

Reload documents while the server is running:

```bash
curl -X POST http://127.0.0.1:8000/api/reload-knowledge
```

Check document index status:

```bash
curl http://127.0.0.1:8000/health
```

Cache official URLs:

```bash
python3 scripts/cache_knowledge_urls.py
```

## 2.1 Enrolled-Student Timetable Support

The chatbot is now designed for two user groups:

- Prospective students who want to apply for MEM or MIM.
- Enrolled students who need timetable, event, course, and deadline help.

The uploaded SS26 Excel timetable was converted into searchable chatbot
knowledge:

```text
knowledge_docs/Semesteruebersicht_SS26.md
```

The timetable contains entries for:

- `MEM / 1`
- `MEM / 2`
- `MIM / 1`
- `MIM / 2`
- `MIM E-Track`

For exact date/group questions, the backend uses a deterministic timetable
lookup instead of relying only on the LLM. Example:

```text
What does MIM E-Track have on Tuesday 24 March 2026?
```

This returns the matching rows from the imported timetable and reminds students
to check email or official announcements for last-minute changes.

Importer script:

```bash
python3 scripts/import_semester_timetable.py "/Users/anukavarsha/Downloads/Semesterübersicht SS26 12.03.xlsx"
```

## 2.2 Email And Deadline Option

For student emails, the safe workflow is to sync only relevant official emails
into a local summary document, then let the chatbot read that summary. The bot
should not continuously read private email in the background.

Recommended approach:

- Search emails only with explicit permission.
- Limit searches to MEM/MIM/course terms, recent dates, or known senders.
- Extract only event names, dates, deadlines, rooms, and official links.
- Save the extracted items into `knowledge_docs/Student_Events_and_Deadlines.md`.
- Reload the chatbot knowledge.

This keeps private email content out of the chatbot unless it is needed for
course support.

## 3. Professor Voice

The chatbot currently uses local XTTS with Raphael's approved reference clip.
The speaker button now calls `/api/voice` on demand. This keeps the chat fast
while preserving the professor-style audio demo.

Current voice mode:

```text
VOICE_PROVIDER=xtts
XTTS_SPEAKER_WAV=voice_source/instant_voice_clone_clips/raphael_10s_45min.mp3
```

The OpenVoiceV2 notebook from the professor can still be tested separately, but
it requires the OpenVoice repository, MeloTTS, and OpenVoiceV2 checkpoints.

## 4. MCP Option

An optional MCP server was added in:

```text
mcp_knowledge_server.py
```

It exposes the local `knowledge_docs` search as an MCP tool:

```text
search_mem_mim_documents
```

The main demo does not depend on MCP, so the chatbot remains stable even if MCP
is not installed. To test MCP separately:

```bash
source .venv/bin/activate
python -m pip install mcp
python mcp_knowledge_server.py
```

