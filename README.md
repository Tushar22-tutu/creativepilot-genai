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


---


