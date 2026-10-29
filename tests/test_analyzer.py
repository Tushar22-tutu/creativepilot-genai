"""Unit tests for the brand-analysis pipeline; no live LLM is required."""

from copy import deepcopy
from unittest.mock import Mock

from backend.brand_intelligence import analyzer
from backend.brand_intelligence.fallback import fallback_brand_profile


VALID_LLM_PROFILE = {
    "brand_voice": "original voice",
    "core_emotions": ["trust", "motivation", "confidence"],
    "target_audience": {
        "age_range": "25-45",
        "pain_points": ["lack of time"],
        "desires": ["convenience", "health"],
    },
    "communication_style": "original style",
    "cta_style": "original CTA",
}


def test_analyze_brand_uses_llm_applies_tone_rules_and_saves(monkeypatch):
    llm = Mock(return_value=deepcopy(VALID_LLM_PROFILE))
    get_memory = Mock(return_value=None)
    save_memory = Mock()
    monkeypatch.setattr(analyzer, "call_llm", llm)
    monkeypatch.setattr(analyzer, "get_brand_from_memory", get_memory)
    monkeypatch.setattr(analyzer, "save_brand_to_memory", save_memory)

    result = analyzer.analyze_brand({"brand_name": "FitSphere", "tone": "premium"})

    llm.assert_called_once()
    get_memory.assert_called_once_with("FitSphere")
    save_memory.assert_called_once_with("FitSphere", result)
    assert result["brand_voice"] == "professional, confident"
    assert result["communication_style"] == "professional, polished"
    assert result["cta_style"] == "subtle, confident"
    assert result["core_emotions"] == ["trust", "motivation"]


def test_analyze_brand_falls_back_when_llm_fails(monkeypatch):
    monkeypatch.setattr(analyzer, "call_llm", Mock(side_effect=RuntimeError("LLM unavailable")))
    monkeypatch.setattr(analyzer, "get_brand_from_memory", Mock(return_value=None))
    save_memory = Mock()
    monkeypatch.setattr(analyzer, "save_brand_to_memory", save_memory)

    result = analyzer.analyze_brand({"brand_name": "FallbackCo", "tone": "casual"})

    assert result["core_emotions"] == fallback_brand_profile()["core_emotions"]
    assert result["communication_style"] == "friendly, conversational"
    assert result["cta_style"] == "light and encouraging"
    save_memory.assert_called_once_with("FallbackCo", result)


def test_analyze_brand_returns_cached_profile_without_calling_llm(monkeypatch):
    cached = fallback_brand_profile()
    llm = Mock()
    save_memory = Mock()
    monkeypatch.setattr(analyzer, "call_llm", llm)
    monkeypatch.setattr(analyzer, "get_brand_from_memory", Mock(return_value=cached))
    monkeypatch.setattr(analyzer, "save_brand_to_memory", save_memory)

    result = analyzer.analyze_brand({"brand_name": "ExistingBrand", "tone": "bold"})

    assert result == cached
    llm.assert_not_called()
    save_memory.assert_not_called()
