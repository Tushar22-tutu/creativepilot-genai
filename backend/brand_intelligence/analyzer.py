from brand_intelligence.prompts import BRAND_ANALYSIS_PROMPT
from utils.llm_client import call_llm

def analyze_brand(brand_input: dict) -> dict:
    prompt = BRAND_ANALYSIS_PROMPT.format(
        brand_input=brand_input
    )

    brand_context = call_llm(prompt)
    return brand_context
