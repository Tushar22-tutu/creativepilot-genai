"""FastAPI contract tests. External LLM and agent calls are mocked."""

from fastapi.testclient import TestClient

from backend import main
from backend.brand_intelligence.fallback import fallback_brand_profile


client = TestClient(main.app)


def test_health_endpoint_returns_running_status():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "CreativePilot API is running"}


def test_analyze_brand_endpoint_returns_valid_profile(monkeypatch):
    expected = fallback_brand_profile()
    monkeypatch.setattr(main, "analyze_brand", lambda payload: expected)

    response = client.post(
        "/analyze-brand",
        json={"brand_name": "FitSphere", "tone": "premium"},
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_analyze_brand_endpoint_rejects_missing_brand_name():
    response = client.post("/analyze-brand", json={"tone": "premium"})

    assert response.status_code == 422


def test_agent_endpoint_returns_agent_result_without_running_llm(monkeypatch):
    expected = {
        "result": fallback_brand_profile(),
        "validated": True,
        "error": None,
        "retries": 0,
    }
    monkeypatch.setattr(main, "run_agent", lambda payload: expected)

    response = client.post(
        "/agent/analyze-brand",
        json={"brand_name": "FitSphere", "tone": "premium"},
    )

    assert response.status_code == 200
    assert response.json() == expected
