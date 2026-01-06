
import requests
import json
import re

USE_LOCAL_LLM = True


def call_llm(prompt: str) -> dict:
    if USE_LOCAL_LLM:
        return call_local_llm(prompt)
    else:
        return mock_llm_response()


# -------- LOCAL LLM (OLLAMA) --------
def call_local_llm(prompt: str) -> dict:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma:2b",
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )

    raw_text = response.json().get("response", "")

    # 🔒 SAFETY: extract JSON only
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if not match:
        raise ValueError("No valid JSON found in LLM response")

    json_text = match.group()
    return json.loads(json_text)


# -------- MOCK (fallback dev mode) --------
def mock_llm_response():
    return {
        "brand_voice": "professional, confident",
        "core_emotions": ["trust", "aspiration"],
        "target_audience": {
            "age_range": "25-40",
            "pain_points": ["lack of time", "work stress"],
            "desires": ["healthy lifestyle", "convenience"]
        },
        "communication_style": "professional, polished",
        "cta_style": "subtle, confident"
    }

