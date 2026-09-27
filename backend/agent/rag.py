"""
Lightweight local RAG over CreativePilot's existing brand context.

No vector database is introduced. Documents (past brand profiles from
brand_memory.json + a handful of static brand-voice notes) are embedded once
with Ollama's embedding endpoint and kept in a plain in-memory list. If the
embedding model isn't available (not pulled, Ollama not running), retrieval
falls back to simple keyword overlap so the agent still gets *some* context
instead of hard-failing -- this fallback path is exercised by
backend/agent/evaluate.py.
"""

import json
import math
import os

from langchain_ollama import OllamaEmbeddings

from backend.brand_intelligence.memory import MEMORY_FILE

EMBED_MODEL = "nomic-embed-text"

# Small static knowledge base seeding retrieval beyond just past brand profiles.
STATIC_BRAND_KNOWLEDGE = [
    "Premium brands favor understated, confident language over hype-driven claims.",
    "Casual brands use conversational tone, contractions, and playful CTAs.",
    "Bold brands lean on high-energy verbs and urgency-driven calls to action.",
    "Consistent brand voice across touchpoints increases audience trust over time.",
]

_embeddings = None
_document_store = []  # [{"text": str, "embedding": list[float] | None}]
_embeddings_available = True


def _get_embeddings() -> OllamaEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    return _embeddings


def _load_brand_documents() -> list:
    docs = list(STATIC_BRAND_KNOWLEDGE)

    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                stored = json.load(f)
            for brand_name, profile in stored.items():
                docs.append(
                    f"Brand '{brand_name}': voice={profile.get('brand_voice')}, "
                    f"style={profile.get('communication_style')}, "
                    f"cta={profile.get('cta_style')}"
                )
        except (json.JSONDecodeError, OSError):
            pass

    return docs


def build_index(force_rebuild: bool = False) -> None:
    """Chunk + embed existing brand context into an in-memory index (once)."""
    global _document_store, _embeddings_available

    if _document_store and not force_rebuild:
        return

    docs = _load_brand_documents()

    try:
        vectors = _get_embeddings().embed_documents(docs)
        _document_store = [{"text": d, "embedding": v} for d, v in zip(docs, vectors)]
        _embeddings_available = True
    except Exception as e:
        print("⚠️ RAG embeddings unavailable, falling back to keyword match:", e)
        _document_store = [{"text": d, "embedding": None} for d in docs]
        _embeddings_available = False


def _cosine_similarity(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _keyword_score(query: str, text: str) -> int:
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())
    return len(query_words & text_words)


def retrieve_context(query: str, top_k: int = 3) -> list:
    """Return the top_k most relevant context chunks for the query."""
    build_index()

    if not _document_store:
        return []

    if _embeddings_available:
        try:
            query_vector = _get_embeddings().embed_query(query)
            scored = [
                (_cosine_similarity(query_vector, doc["embedding"]), doc["text"])
                for doc in _document_store
            ]
        except Exception as e:
            print("⚠️ RAG query embedding failed, falling back to keyword match:", e)
            scored = [(_keyword_score(query, doc["text"]), doc["text"]) for doc in _document_store]
    else:
        scored = [(_keyword_score(query, doc["text"]), doc["text"]) for doc in _document_store]

    scored.sort(key=lambda x: x[0], reverse=True)
    return [text for score, text in scored[:top_k] if score > 0]
