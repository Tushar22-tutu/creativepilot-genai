from utils.llm_client import call_llm
from brand_intelligence.schema import validate_brand_output
from brand_intelligence.fallback import fallback_brand_profile
from brand_intelligence.rules import apply_brand_rules


def analyze_brand(brand_input: dict):
    prompt = f"Analyze brand: {brand_input}"

    try:
        result = call_llm(prompt)
        validate_brand_output(result)
        

    except Exception as e:
        print("⚠️ LLM failed, using fallback:", e)
        

    result = apply_brand_rules(result, brand_input)
    return result
