from fastapi import FastAPI
from brand_intelligence.analyzer import analyze_brand
from brand_intelligence.schemas import BrandInput, BrandOutput
from brand_intelligence.memory import load_memory_from_file

# -----------------------------
# FastAPI App Initialization
# -----------------------------
app = FastAPI(
    title="CreativePilot GenAI API",
    description="GenAI-driven brand intelligence and ad strategy engine",
    version="1.0.0"
)

# -----------------------------
# Load persisted brand memory
# (runs once when server starts)
# -----------------------------
load_memory_from_file()


# -----------------------------
# Health Check Endpoint
# -----------------------------
@app.get("/")
def health_check():
    return {"status": "CreativePilot API is running"}


# -----------------------------
# Brand Analysis Endpoint
# -----------------------------
@app.post("/analyze-brand", response_model=BrandOutput)
def analyze_brand_api(brand_input: BrandInput):
    """
    Analyze brand input and return a consistent brand profile.
    """
    # Convert Pydantic model to dict for internal processing
    brand_data = brand_input.dict()

    result = analyze_brand(brand_data)
    return result

