def normalize_tone(tone: str) -> str:
    tone = tone.lower()

    if tone in ["professional", "corporate", "formal", "premium"]:
        return "premium"
    if tone in ["friendly", "casual", "relaxed"]:
        return "casual"
    if tone in ["bold", "aggressive", "energetic"]:
        return "bold"

    return "casual"


def apply_brand_rules(data: dict, brand_input: dict) -> dict:
    raw_tone = brand_input.get("tone", "")
    tone = normalize_tone(raw_tone)

    

    if tone == "premium":
        data["brand_voice"] = "professional, confident"
        data["communication_style"] = "professional, polished"
        data["cta_style"] = "subtle, confident"

    elif tone == "casual":
        data["communication_style"] = "friendly, conversational"
        data["cta_style"] = "light and encouraging"

    elif tone == "bold":
        data["communication_style"] = "energetic, confident"
        data["cta_style"] = "strong and action-oriented"

    if isinstance(data.get("core_emotions"), list):
        data["core_emotions"] = data["core_emotions"][:2]

    return data
