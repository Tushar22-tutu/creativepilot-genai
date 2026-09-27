"""
LangChain tools for the agentic layer. Each tool is a thin wrapper around
existing CreativePilot functionality -- no business logic is duplicated
here.
"""

import json

from langchain_core.tools import tool

from backend.agent.rag import retrieve_context
from backend.brand_intelligence.analyzer import analyze_brand
from backend.brand_intelligence.memory import get_brand_from_memory, save_brand_to_memory


@tool
def retrieve_brand_context(brand_name: str) -> str:
    """Look up a previously analyzed brand profile from persistent memory, if one exists."""
    cached = get_brand_from_memory(brand_name)
    if not cached:
        return json.dumps({"found": False})
    return json.dumps({"found": True, "profile": cached})


@tool
def analyze_brand_tool(
    brand_name: str,
    product: str = "",
    target_audience: str = "",
    tone: str = "professional",
) -> str:
    """Run CreativePilot's existing brand analysis pipeline (LLM + rules + fallback)
    for a brand and return its structured JSON profile."""
    result = analyze_brand(
        {
            "brand_name": brand_name,
            "product": product,
            "target_audience": target_audience,
            "tone": tone,
        }
    )
    return json.dumps(result)


@tool
def retrieve_rag_context(query: str) -> str:
    """Retrieve relevant brand-strategy context (past brand profiles + brand-voice
    guidance) for a query."""
    chunks = retrieve_context(query)
    if not chunks:
        return "No relevant context found."
    return "\n".join(f"- {c}" for c in chunks)


@tool
def save_brand_memory(brand_name: str, brand_profile: dict) -> str:
    """Persist a brand profile to memory so future requests for the same brand reuse it."""
    save_brand_to_memory(brand_name, brand_profile)
    return f"Saved profile for '{brand_name}' to memory."


AGENT_TOOLS = [retrieve_brand_context, analyze_brand_tool, retrieve_rag_context, save_brand_memory]
