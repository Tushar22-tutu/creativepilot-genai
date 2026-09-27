from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.brand_intelligence.analyzer import analyze_brand
from backend.brand_intelligence.schemas import BrandInput, BrandOutput
from backend.brand_intelligence.memory import load_memory_from_file
from backend.agent.graph import run_agent  # ADDED: agentic layer


app = FastAPI(
    title="CreativePilot GenAI API",
    description="GenAI-driven brand intelligence and ad strategy engine",
    version="1.0.0"
)

# Load memory on startup
load_memory_from_file()

# CORS middleware (MANDATORY for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "CreativePilot API is running"}

@app.post("/analyze-brand", response_model=BrandOutput)
def analyze_brand_api(brand_input: BrandInput):
    return analyze_brand(brand_input.dict())

# ADDED: agentic route (LangGraph + tools + RAG). Existing /analyze-brand
# above is untouched and keeps using the original non-agentic pipeline.
@app.post("/agent/analyze-brand")
def analyze_brand_agentic(brand_input: BrandInput):
    return run_agent(brand_input.dict())
