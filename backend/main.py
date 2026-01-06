from fastapi import FastAPI
from brand_intelligence.analyzer import analyze_brand
from brand_intelligence.schemas import BrandInput, BrandOutput

app = FastAPI(
    title="CreativePilot GenAI API",
    description="GenAI-driven brand intelligence and ad strategy engine",
    version="1.0.0"
)


@app.get("/")
def health_check():
    return {"status": "CreativePilot API is running"}


@app.post("/analyze-brand", response_model=BrandOutput)
def analyze_brand_api(brand_input: BrandInput):
    """
    Analyze brand input and return a consistent brand profile.
    """
    # Pydantic model -> dict for internal logic
    brand_data = brand_input.dict()

    result = analyze_brand(brand_data)
    return result

