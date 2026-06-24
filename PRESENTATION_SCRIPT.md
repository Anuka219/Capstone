# MEM & MIM Guide Bot — 5-Minute Presentation Script

*Total ≈ 5–5.5 minutes (the MCP slide adds ~45s — trim the demo or a section if
you need a hard 5:00). The same text is attached to each slide as Speaker Notes
(visible in PowerPoint's **Notes pane** / **Presenter View**). Speak one slide
at a time; aim for a calm, even pace (~140 words/min).*

---

## Slide 1 — Title  ·  ~0:25
Good morning. We're **[your names]**, and our capstone is the **MEM & MIM Guide
Bot** — an AI chatbot we built to answer student questions about Hochschule
Pforzheim's two master's programs: **Engineering & Management (MEM)** and
**Industrial Management (MIM)**. In the next five minutes we'll show what it
does, how we built it, the tools we used, the main challenges we solved — and
finish with a quick live demo.

## Slide 2 — What We Built  ·  ~0:55
So what is it? A chatbot that answers questions about MEM and MIM in plain
language — which program fits you, the courses, careers, how to apply, fees, and
language requirements. It has **two modes**: a *prospective-student* mode for
people deciding whether to apply, and an *enrolled-student* mode for current
students who need help with classes and their schedule. A key design goal: it
gives **direct, grounded answers** — for facts like schedules, rooms, professors
and deadlines it pulls from fixed, reliable sources instead of guessing. And it
has **voice output** in the professor's voice plus a simple web interface, so
it's easy to demo and use.

## Slide 3 — Implementation  ·  ~0:55
Here's how it's built. The **frontend** is a single-page web interface —
`index.html` — where the user types and reads answers. It talks to a **backend**
server we wrote in Python with FastAPI, in `app.py`, which handles routing and
logic. Behind that is our **knowledge base**: curated facts, the timetable, room
data, and course-to-professor data. The important decision is on the right — the
**Groq language model is used only when a flexible, conversational explanation is
needed**. For anything factual, the answer comes from those fixed sources. That
separation is what keeps the bot accurate instead of making things up.

## Slide 4 — Tools Used  ·  ~0:40
The tools: **Python with FastAPI** for the chatbot's API and server. Standard
**HTML, CSS and JavaScript** for the browser experience. **Groq's LLM** for the
conversational answers, and **ElevenLabs** for the optional voice output. And we
built **PDF extraction** to pull room and professor information out of the
university's timetable PDFs into clean, searchable data.

## Slide 5 — Methodology & Challenges  ·  ~1:00
Our method was straightforward: a brief analysis of what students actually ask,
then collecting the facts, then building the backend and frontend, and finally a
lot of testing for accuracy. **Two challenges** stood out. First, **avoiding
hallucinated facts** — language models can sound confident and still be wrong, so
for schedules, rooms, fees and language requirements we force the bot to use
fixed sources, and if it doesn't have something it says *"I don't have that"*
rather than inventing an answer. Second, the **timetable PDFs were messy** — room
and professor data came in different formats across documents — so we built
custom extraction to turn that into clean data the bot can search reliably.

## Slide 6 — MCP (Model Context Protocol)  ·  ~0:50
You asked us to try **MCP** — the Model Context Protocol — and we did, in **two
ways**. First, we built an **MCP server** (`mcp_knowledge_server.py`) that exposes
our knowledge base as an MCP tool, `search_mem_mim_documents`, so any MCP host —
like Claude Desktop — can query our MEM/MIM data. Second — and this is the part
you can **see live** — we wired that exact same tool into the bot: type
**`mcp search: <topic>`** in the chat and it runs the MCP knowledge search and
returns the sourced excerpts straight from our documents. So MCP isn't just theory
here — the tool runs in the demo. (A full external MCP client connection needs
`pip install mcp`, but the search tool is the same either way.)

## Slide 7 — Live Demo / Thank You  ·  ~0:45 + demo
And that brings us to the **live demo**. *(Switch to the bot.)* Let me ask it a
few things — how to apply, the difference between MEM and MIM, and a schedule
question — and, to show **MCP**, type **`mcp search: MIM English Track language
requirements`** so you can see the MCP tool return sourced excerpts live. *(Run
the demo — one question at a time.)* … That's the MEM & MIM Guide Bot. We built it ourselves,
with help from **AI pair-programming assistants — Claude (Claude Code) and
Codex** — for coding, debugging and testing; the direction and decisions are
ours. **Thank you — we're happy to take any questions.**

---

### Demo tips
- **Warm it up** a minute before (first voice click + first question are the slow ones).
- **Ask one question at a time** (the free LLM tier is rate-limited).
- Good demo questions: *"How do I apply for MIM?"* · *"Compare MEM and MIM"* ·
  *"Do I need German for the English track?"* · *"What's my class on Tuesday?"*
- **To show MCP live:** type `mcp search: MIM English Track language requirements`
  — it returns excerpts via the MCP knowledge tool (works on the deployed bot too).
- If it ever shows a "busy, ask again" message, just wait ~10s and re-ask.
