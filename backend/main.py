from fastapi import FastAPI
from brand_intelligence.analyzer import analyze_brand

app = FastAPI(title="CreativePilot API")


@app.post("/analyze-brand")
def analyze_brand_api(brand_input: dict):
    return analyze_brand(brand_input)

