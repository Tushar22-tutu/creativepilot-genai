# 🚀 CreativePilot – GenAI Brand Intelligence Platform

CreativePilot is a **full-stack GenAI-powered application** that analyzes brand inputs and generates a **consistent, structured brand identity** using a combination of **local LLMs, prompt engineering, business rules, memory persistence, and a modern API architecture**.

This project focuses on **controlling AI outputs** rather than blindly generating text, making it suitable for **real-world, production-grade GenAI systems**.

---

## 🧠 Key Problem Solved

Traditional LLM usage suffers from:
- Inconsistent brand tone across requests  
- Unstructured / unpredictable outputs  
- Over-reliance on paid APIs  
- No memory of past brand identity  

**CreativePilot solves this by combining AI with backend discipline.**

---

## 🏗️ System Architecture
```
React Frontend
↓
FastAPI Backend
↓
Pydantic Validation
↓
Brand Analyzer (Core Logic)
↓
Memory Layer (Persistent)
↓
Prompt Engineering
↓
Local LLM (Ollama)
↓
Rules Engine + Fallback
↓
Structured Brand Output
```
---

## ✨ Core Features

### 🔹 Brand Intelligence Engine
- Generates brand voice, emotions, communication style, and CTA
- Output is always **structured JSON**

### 🔹 Prompt Engineering
- Strict prompts to enforce schema-based output
- Prevents hallucinated or free-text responses

### 🔹 Local LLM (Ollama)
- No paid API dependency
- Fully offline and cost-free
- Model-agnostic architecture

### 🔹 Memory Layer (Persistent)
- Brand identity is stored and reused
- Ensures **same brand = same output**, even after server restart

### 🔹 Fallback Mechanism
- System never crashes due to AI failure
- Safe defaults are returned if LLM output is invalid

### 🔹 FastAPI + Pydantic
- Strict input/output validation
- Auto-generated Swagger documentation
- Clean API contracts for frontend consumption

### 🔹 React Frontend
- Lightweight UI to interact with backend
- Uses React functional components and `useState`
- Backend remains the primary intelligence layer

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Pydantic
- Ollama (Local LLM)

### Frontend
- React (Vite)
- JavaScript
- Fetch API

### DevOps / Tooling
- Git & GitHub
- Modular project structure
- `.gitignore` for clean repository hygiene

---

## 📂 Project Structure
```
CreativePilot/
├── backend/
│ ├── main.py
│ ├── brand_intelligence/
│ │ ├── analyzer.py
│ │ ├── memory.py
│ │ ├── schemas.py
│ │ └── init.py
│ └── utils/
│ └── llm_client.py
│
├── frontend/
│ ├── src/
│ │ ├── App.jsx
│ │ ├── main.jsx
│ │ └── styles
│ ├── index.html
│ └── package.json
│
├── .gitignore
└── README.md

```
---

## 🚀 How to Run the Project

### 1️⃣ Start Backend
```bash
cd CreativePilot
py -m uvicorn backend.main:app --reload
```

Open:

http://127.0.0.1:8000/docs

### 2️⃣ Start Frontend
```
cd frontend
npm install
npm run dev
```

Open:

http://localhost:5173
### 🧪 Example Input
```

{
  "brand_name": "FitSphere",
  "product": "Online fitness coaching",
  "target_audience": "Working professionals",
  "tone": "premium"
}
```

### ✅ Example Output
```

{
  "brand_voice": "professional, confident",
  "core_emotions": ["motivation", "trust"],
  "target_audience": {
    "age_range": "25-45",
    "pain_points": ["lack of time", "low energy"],
    "desires": ["healthy lifestyle", "convenience"]
  },
  "communication_style": "polished, professional",
  "cta_style": "subtle, confident"
}
```

### 🎯 Design Philosophy

- AI is not trusted blindly

- Business rules have final authority

- Backend owns intelligence, frontend only consumes

- Fail-safe architecture over fancy generation

“AI can fail. The system should not.”

### 🧠 Interview Highlights

- Local LLM usage instead of paid APIs

- Prompt engineering + schema validation

- Persistent memory for consistency

- Production-style FastAPI backend

- Clean separation of frontend and backend

---

## 🤖 Agentic Layer (added)

A small agentic layer sits *around* the original pipeline above without
changing it. `/analyze-brand` still works exactly as before; a new
`/agent/analyze-brand` endpoint runs the same brand analysis through a
LangGraph agent that can decide to check memory, pull RAG context, and call
the analysis pipeline as a tool.

```
POST /agent/analyze-brand
        ↓
   LangGraph Agent (Ollama, tool-calling model)
        ↓
   Decide: need a tool?
        ├─ retrieve_brand_context   → existing memory.py
        ├─ retrieve_rag_context     → new lightweight local RAG
        ├─ analyze_brand_tool       → existing analyzer.py pipeline
        └─ save_brand_memory        → existing memory.py
        ↓
   Generate structured response
        ↓
   Pydantic validation (existing BrandOutput schema)
        ↓
   Retry once → Fallback to existing safe defaults if still invalid
        ↓
   END
```

### New components
- **LangGraph workflow** (`backend/agent/graph.py`) — the stateful agent graph shown above. Reuses `analyzer.py`, `memory.py`, `fallback.py`, and `schemas.py` unchanged; adds an outer Pydantic-validation retry/fallback loop on top of the analyzer's own internal one.
- **Tool calling** (`backend/agent/tools.py`) — 4 LangChain tools, each a thin wrapper over an existing function, that the Ollama agent model calls itself: `retrieve_brand_context`, `analyze_brand_tool`, `retrieve_rag_context`, `save_brand_memory`.
- **Persistent brand memory** — the existing `memory.py` JSON-file store (`brand_memory.json`) is reused as-is; the agent reads it via `retrieve_brand_context` and writes to it via `save_brand_memory`, so brand profiles the agent produces persist across restarts exactly like the original pipeline's.
- **Lightweight local RAG** (`backend/agent/rag.py`) — no vector database. Chunks are past brand profiles (from `brand_memory.json`) plus a few static brand-voice notes, embedded once via Ollama embeddings and kept in a plain in-memory list with cosine similarity. If the embedding model isn't available, it falls back to keyword overlap so retrieval never hard-fails.
- **Ollama local LLM** (`backend/agent/llm.py`) — a separate `ChatOllama` instance using a tool-calling-capable model (`llama3.1` by default — pull it with `ollama pull llama3.1`, or swap the constant for another tool-calling model you have). The original pipeline keeps using `gemma:2b` via `utils/llm_client.py` unchanged, since that model isn't reliable at tool calling.
- **Pydantic validation + retry/fallback** (`backend/agent/graph.py`) — the agent's final structured output is checked against the existing `BrandOutput` schema; on failure it gets one retry through the agent, then falls back to the existing `fallback_brand_profile()`.
- **FastMCP server** (`backend/mcp_server.py`) — a small, separate MCP server exposing `get_brand_context`, `analyze_brand`, and `save_brand_memory` over MCP, each calling the real existing functions. Run it with `python -m backend.mcp_server`. It's a standalone process — it doesn't replace or duplicate the FastAPI app.
- **Evaluation script** (`backend/agent/evaluate.py`) — 6 scenarios: normal request, tool-call-required request, RAG-benefiting request, invalid tool output (retry/fallback), tool failure, and multi-turn (same brand run twice). Run with `python -m backend.agent.evaluate` (requires Ollama running locally with the agent model pulled).
- **New endpoint** — `POST /agent/analyze-brand` runs the above. The original `POST /analyze-brand` endpoint is untouched and keeps using the original non-agentic pipeline exactly as before.

### Example tool-calling flow
1. Request comes in for brand `"FitSphere"`.
2. Agent calls `retrieve_brand_context("FitSphere")` — memory has nothing yet.
3. Agent calls `analyze_brand_tool(...)`, which runs the existing pipeline (LLM → rules → fallback) and returns a JSON profile.
4. The graph validates that JSON against `BrandOutput`. If valid, it's returned; if not, the agent gets one retry, then the existing `fallback_brand_profile()` is used.

### Running it
```bash
# 1. Ollama running locally, with both models pulled:
ollama pull gemma:2b       # used by the original /analyze-brand pipeline
ollama pull llama3.1       # used by the new agentic layer (needs tool calling)

# 2. Install deps (no requirements.txt existed before this change)
pip install -r requirements.txt

# 3. Run the API as before
py -m uvicorn backend.main:app --reload
# now try POST /agent/analyze-brand at http://127.0.0.1:8000/docs

# 4. (Optional) run the standalone MCP server
python -m backend.mcp_server

# 5. (Optional) run the evaluation scenarios
python -m backend.agent.evaluate
```

### 🔮 Future Enhancements

- Database-backed memory (Redis / PostgreSQL)

- User-specific brand profiles

- Rate limiting & authentication

- Deployment on cloud platforms

### 👨‍💻 Author

Tushar Walia
Full-Stack & GenAI Enthusiast

### ⭐ Final Note

CreativePilot is not just a demo —
it is a foundation for building real, controllable GenAI systems.
