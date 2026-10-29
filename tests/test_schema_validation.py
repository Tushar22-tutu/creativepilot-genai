"""Tests for the lightweight dictionary validator used before returning LLM data."""

import pytest

from backend.brand_intelligence.schema import validate_brand_output


VALID_PROFILE = {
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


def test_validator_accepts_complete_profile():
    assert validate_brand_output(VALID_PROFILE) is True


def test_validator_rejects_non_dictionary():
    with pytest.raises(ValueError, match="not a dictionary"):
        validate_brand_output(["not", "a", "dictionary"])


def test_validator_rejects_missing_field():
    incomplete = dict(VALID_PROFILE)
    incomplete.pop("cta_style")

    with pytest.raises(ValueError, match="Missing required field: cta_style"):
        validate_brand_output(incomplete)


def test_validator_rejects_wrong_field_type():
    invalid = {**VALID_PROFILE, "core_emotions": "trust"}

    with pytest.raises(TypeError, match="core_emotions"):
        validate_brand_output(invalid)
