# Knowledge Documents

Put official MEM/MIM PDFs, DOCX, TXT, Markdown, or HTML files in this folder.
The chatbot reads this folder at startup and uses the most relevant excerpts
when answering precise factual questions.

## Cache Official Web Pages

Instead of live scraping during each question, cache official pages once:

1. Add official URLs to:

```text
knowledge_docs/source_urls.txt
```

2. Run:

```bash
python3 scripts/cache_knowledge_urls.py
```

This saves local HTML copies in:

```text
knowledge_docs/web_cache/
```

3. Reload the chatbot knowledge:

```bash
curl -X POST http://127.0.0.1:8000/api/reload-knowledge
```

Use this for official program pages, timetable pages, module handbook pages,
application pages, deadlines, contact pages, and FAQ pages.

After adding or replacing files while the server is running, reload the index:

```bash
curl -X POST http://127.0.0.1:8000/api/reload-knowledge
```

Supported directly:

- `.txt`
- `.md`
- `.html`
- `.docx`

PDF support needs a PDF reader package such as `pypdf` or `PyPDF2`.
