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

from mcp.server.fastmcp import FastMCP

from app import KNOWLEDGE_DIR, load_knowledge_documents, search_knowledge


mcp = FastMCP("mem-mim-knowledge")


@mcp.tool()
def search_mem_mim_documents(question: str, limit: int = 4) -> str:
    """Search local MEM/MIM PDFs and documents for relevant excerpts."""
    load_knowledge_documents()
    matches = search_knowledge(question, limit=limit)
    if not matches:
        return f"No relevant local document excerpts found in {KNOWLEDGE_DIR}."

    parts = []
    for index, match in enumerate(matches, 1):
        parts.append(f"Source {index}: {match['source']}\n{match['text']}")
    return "\n\n".join(parts)


if __name__ == "__main__":
    mcp.run()

