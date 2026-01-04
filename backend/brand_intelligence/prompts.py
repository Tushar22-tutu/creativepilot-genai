BRAND_ANALYSIS_PROMPT = """
You are an expert brand strategist.

Analyze the following brand details and generate a structured brand profile.

Return ONLY valid JSON with these exact fields:
- brand_voice
- core_emotions
- target_audience (age_range, pain_points, desires)
- communication_style
- cta_style

Brand Details:
{brand_input}

Rules:
- Be realistic and professional
- Do NOT add explanations
- Do NOT add extra fields
- Return ONLY JSON
"""
