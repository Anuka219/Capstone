#!/usr/bin/env python3
"""
Optional MCP server for the MEM & MIM Guide Bot knowledge base.

The main chatbot does not require MCP. This file is an optional extension that
exposes the same local `knowledge_docs` search as an MCP tool.

Install only if you want to demo MCP separately:

    source .venv/bin/activate
    python -m pip install mcp
    python mcp_knowledge_server.py
"""

from __future__ import annotations

import re

import app


try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:
    FastMCP = None


def search_mem_mim_documents(question: str, limit: int = 4) -> str:
    """Search local MEM/MIM PDFs and documents for relevant excerpts."""
    clean = question.lower()
    terms = {
        term
        for term in re.findall(r"[a-zA-ZÄÖÜäöüß0-9]{3,}", clean)
        if term not in {"what", "when", "where", "which", "with", "about", "that", "this", "from"}
    }
    if not terms:
        return "Please provide a search topic."

    app.load_knowledge_documents()
    wants_facts = re.search(r"\b(language|german|english|ielts|toefl|fee|fees|tuition|application|admission|deadline)\b", clean)
    wants_schedule = re.search(r"\b(schedule|timetable|room|class|professor|teacher|lecture)\b", clean)

    ranked = []
    for chunk in app.knowledge_chunks:
        text = chunk["text"].lower()
        source = chunk["source"]
        source_lower = source.lower()
        score = sum(text.count(term) * 2 + source_lower.count(term) for term in terms)
        if not score:
            continue
        if wants_facts and "MEM_MIM_curated_facts" in source:
            score += 100
        if wants_facts and "timetable" in source_lower:
            score -= 25
        if wants_schedule and (
            "timetable" in source_lower
            or "semesteruebersicht" in source_lower
            or "course_professors" in source_lower
        ):
            score += 100
        ranked.append((score, chunk))

    if not ranked:
        return f"No relevant local document excerpts found in {app.KNOWLEDGE_DIR}."

    ranked.sort(key=lambda item: item[0], reverse=True)
    matches = [chunk for _score, chunk in ranked[:limit]]

    parts = []
    for index, match in enumerate(matches, 1):
        parts.append(f"Source {index}: {match['source']}\n{match['text']}")
    return "\n\n".join(parts)


mcp = FastMCP("mem-mim-knowledge") if FastMCP else None
if mcp:
    mcp.tool()(search_mem_mim_documents)


if __name__ == "__main__":
    if not mcp:
        raise SystemExit(
            "The optional 'mcp' package is not installed. Install it with "
            "`python -m pip install mcp` to run this as an MCP server."
        )
    mcp.run()
