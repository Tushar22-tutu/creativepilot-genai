"""
Small evaluation script for the agentic layer. Requires Ollama running
locally with backend/agent/llm.py's AGENT_MODEL pulled. Mirrors the simple,
print-based style of the existing backend/test_brand_analysis.py.

Run directly:

    python -m backend.agent.evaluate

Covers:
  1. Normal request
  2. Request requiring a tool call
  3. Request that benefits from RAG context
  4. Invalid LLM output (forces the retry/fallback path)
  5. Tool failure (forces the ToolNode's built-in error handling)
  6. Multi-turn interaction (same brand run twice; second should hit memory)
"""

from unittest.mock import patch

from backend.agent.graph import run_agent

SAMPLE_BRAND = {
    "brand_name": "FitSphere",
    "product": "Online fitness coaching",
    "target_audience": "Working professionals",
    "tone": "premium",
}


def scenario_normal_request():
    print("\n--- Scenario 1: Normal request ---")
    result = run_agent(SAMPLE_BRAND)
    print(result)


def scenario_tool_call_required():
    print("\n--- Scenario 2: Requires analyze_brand_tool ---")
    result = run_agent(
        {
            "brand_name": "NovaWear",
            "product": "Sustainable streetwear",
            "target_audience": "Gen Z shoppers",
            "tone": "bold",
        }
    )
    print(result)


def scenario_rag_required():
    print("\n--- Scenario 3: Benefits from RAG context ---")
    result = run_agent(
        {
            "brand_name": "CalmRoots",
            "product": "Herbal tea subscription",
            "target_audience": "Stressed professionals",
            "tone": "casual",
        }
    )
    print(result)


def scenario_invalid_llm_output():
    print("\n--- Scenario 4: Invalid tool output triggers retry/fallback ---")
    # Patched at backend.agent.tools.analyze_brand (the name bound inside
    # tools.py via `from ... import analyze_brand`), not at the original
    # definition in analyzer.py -- patching the definition site would not
    # affect tools.py's already-bound reference.
    with patch(
        "backend.agent.tools.analyze_brand",
        return_value={"brand_voice": "incomplete"},  # missing required fields
    ):
        result = run_agent(
            {
                "brand_name": "GlitchCo",
                "product": "Testing edge cases",
                "target_audience": "QA engineers",
                "tone": "casual",
            }
        )
    print(result)
    assert result["result"] is not None, "Fallback should still return a profile"
    assert result["validated"] is True, "Fallback result should be marked validated"


def scenario_tool_failure():
    print("\n--- Scenario 5: Tool raises an exception ---")
    with patch(
        "backend.agent.tools.analyze_brand",
        side_effect=RuntimeError("Simulated tool crash"),
    ):
        result = run_agent(
            {
                "brand_name": "CrashTest",
                "product": "Failure simulation",
                "target_audience": "Developers",
                "tone": "casual",
            }
        )
    print(result)


def scenario_multi_turn():
    print("\n--- Scenario 6: Multi-turn (same brand twice) ---")
    first = run_agent(SAMPLE_BRAND)
    second = run_agent(SAMPLE_BRAND)
    print("First run:", first)
    print("Second run:", second)


if __name__ == "__main__":
    scenario_normal_request()
    scenario_tool_call_required()
    scenario_rag_required()
    scenario_invalid_llm_output()
    scenario_tool_failure()
    scenario_multi_turn()
    print("\n✅ Evaluation script completed.")
