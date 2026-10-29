"""Unit tests for CreativePilot request/response schemas."""

import pytest
from pydantic import ValidationError

from backend.brand_intelligence.schemas import BrandInput, BrandOutput


def test_brand_input_accepts_valid_payload():
    payload = BrandInput(
        brand_name="FitSphere",
        product="Online fitness coaching",
        target_audience="Working professionals",
        tone="premium",
    )

    assert payload.brand_name == "FitSphere"
    assert payload.tone == "premium"


def test_brand_input_requires_brand_name():
    with pytest.raises(ValidationError):
        BrandInput(product="Online fitness coaching")


def test_brand_output_accepts_valid_profile():
    profile = {
        "brand_voice": "professional, confident",
        "core_emotions": ["trust", "motivation"],
        "target_audience": {
            "age_range": "25-45",
            "pain_points": ["lack of time"],
            "desires": ["convenience"],
        },
        "communication_style": "polished, professional",
        "cta_style": "subtle, confident",
    }

    validated = BrandOutput(**profile)

    assert validated.brand_voice == "professional, confident"
    assert validated.target_audience.age_range == "25-45"


def test_brand_output_rejects_missing_required_field():
    with pytest.raises(ValidationError):
        BrandOutput(brand_voice="professional")
