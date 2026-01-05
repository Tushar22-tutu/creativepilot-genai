
import random


USE_LOCAL_LLM = False   


def call_llm(prompt: str) -> dict:
    """
    Central LLM access point.
    Currently runs in SAFE MOCK MODE.
    """

    if USE_LOCAL_LLM:
        return call_local_llm(prompt)
    else:
        return mock_llm_response(prompt)



def mock_llm_response(prompt: str) -> dict:
    """
    Simulated LLM response.
    Returns dynamic but schema-valid output.
    """

    tones = [
        "premium, confident",
        "bold, energetic",
        "friendly, professional"
    ]

    emotions = [
        ["trust", "aspiration"],
        ["confidence", "energy"],
        ["comfort", "reliability"]
    ]

    return {
        "brand_voice": random.choice(tones),
        "core_emotions": random.choice(emotions),
        "target_audience": {
            "age_range": "25-40",
            "pain_points": ["lack of time", "work stress"],
            "desires": ["healthy lifestyle", "convenience"]
        },
        "communication_style": "clear, professional",
        "cta_style": "encouraging"
    }


def call_local_llm(prompt: str) -> dict:
    """
    Placeholder for Ollama / local LLM.
    NOT USED right now.
    """
    raise NotImplementedError("Local LLM not enabled yet")


