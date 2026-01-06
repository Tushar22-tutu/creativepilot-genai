def build_brand_analysis_prompt(brand_input: dict) -> str:
    """
    Builds a strict prompt for local LLMs (Ollama).
    Forces JSON-only output.
    """

    return f"""
You are a backend AI service.

TASK:
Analyze the brand input and return ONLY a valid JSON object.

STRICT RULES (MANDATORY):
- Output ONLY JSON
- No explanation
- No markdown
- No extra text before or after JSON
- Keys must EXACTLY match this schema

SCHEMA:
{{
  "brand_voice": "string",
  "core_emotions": ["string"],
  "target_audience": {{
    "age_range": "string",
    "pain_points": ["string"],
    "desires": ["string"]
  }},
  "communication_style": "string",
  "cta_style": "string"
}}

Brand Input:
{brand_input}

REMEMBER:
Return ONLY the JSON object.
"""

