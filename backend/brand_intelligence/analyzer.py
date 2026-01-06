from utils.llm_client import call_llm
from brand_intelligence.schema import validate_brand_output
from brand_intelligence.fallback import fallback_brand_profile
from brand_intelligence.rules import apply_brand_rules
from brand_intelligence.prompts import build_brand_analysis_prompt
from brand_intelligence.memory import (
    get_brand_from_memory,
    save_brand_to_memory
)



def analyze_brand(brand_input: dict) -> dict:
    brand_name = brand_input.get("brand_name")

    # 1️⃣ Check memory first
    if brand_name:
        cached = get_brand_from_memory(brand_name)
        if cached:
            return cached

    # 2️⃣ Normal flow (LLM + fallback)
    prompt = build_brand_analysis_prompt(brand_input)

    try:
        result = call_llm(prompt)
        validate_brand_output(result)
    except Exception as e:
        print("⚠️ LLM failed, using fallback:", e)
        result = fallback_brand_profile()

    result = apply_brand_rules(result, brand_input)

    # 3️⃣ Save to memory
    if brand_name:
        save_brand_to_memory(brand_name, result)

    return result
