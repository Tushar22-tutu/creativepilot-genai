"""
LangChain-wrapped local Ollama LLM for the agentic layer ONLY.

Kept fully separate from backend/utils/llm_client.py, which the original
/analyze-brand endpoint keeps using untouched (raw requests + regex JSON
extraction against "gemma:2b").

The agent needs a model that supports Ollama's tool-calling API, which
"gemma:2b" does not reliably do. AGENT_MODEL defaults to "llama3.1" -- pull
it locally with `ollama pull llama3.1`, or change the constant below to any
other tool-calling-capable model you already have pulled (e.g. "qwen2.5",
"mistral-nemo").
"""

from langchain_ollama import ChatOllama

AGENT_MODEL = "llama3.1"


def get_agent_llm(temperature: float = 0.2) -> ChatOllama:
    """Return a fresh ChatOllama instance for the LangGraph agent."""
    return ChatOllama(model=AGENT_MODEL, temperature=temperature)
