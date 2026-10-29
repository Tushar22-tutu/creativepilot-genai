"""Tests for deterministic tone rules used after brand generation."""

import pytest

from backend.brand_intelligence.rules import apply_brand_rules, normalize_tone


@pytest.mark.parametrize(
    ("input_tone", "expected"),
    [
        ("premium", "premium"),
        ("corporate", "premium"),
        ("friendly", "casual"),
        ("relaxed", "casual"),
        ("bold", "bold"),
        ("energetic", "bold"),
        ("unknown-tone", "casual"),
    ],
)
def test_normalize_tone(input_tone, expected):
    assert normalize_tone(input_tone) == expected


@pytest.mark.parametrize(
    ("tone", "expected_style", "expected_cta"),
    [
        ("premium", "professional, polished", "subtle, confident"),
        ("casual", "friendly, conversational", "light and encouraging"),
        ("bold", "energetic, confident", "strong and action-oriented"),
    ],
)
def test_apply_brand_rules_sets_consistent_style(tone, expected_style, expected_cta):
    profile = {
        "brand_voice": "initial voice",
        "core_emotions": ["trust", "motivation", "confidence"],
        "target_audience": {},
        "communication_style": "initial style",
        "cta_style": "initial CTA",
    }

    result = apply_brand_rules(profile, {"tone": tone})

    assert result["communication_style"] == expected_style
    assert result["cta_style"] == expected_cta
    assert result["core_emotions"] == ["trust", "motivation"]


def test_apply_brand_rules_returns_the_supplied_profile():
    profile = {"core_emotions": ["trust"]}

    assert apply_brand_rules(profile, {"tone": "casual"}) is profile
