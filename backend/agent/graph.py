"""
Small stateful LangGraph workflow around the existing CreativePilot
generation flow.

    START -> analyze_request -> agent -> (tools? -> agent)* -> generate_response
          -> validate -> (retry -> agent) | (fallback) | END

The agent decides, via tool calling, whether it needs memory (
retrieve_brand_context), extra context (retrieve_rag_context), and/or to
actually run the analysis (analyze_brand_tool). generate_response always
guarantees a structured result by falling back to a direct analyze_brand_tool
call if the agent never made one. validate re-checks the final result
against the existing Pydantic BrandOutput schema; on failure it retries once
through the agent, then falls back to the existing safe-default profile.
"""

import json
from typing import Optional, TypedDict

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from backend.agent.llm import get_agent_llm
from backend.agent.tools import AGENT_TOOLS, analyze_brand_tool
from backend.brand_intelligence.fallback import fallback_brand_profile
from backend.brand_intelligence.schemas import BrandOutput

MAX_RETRIES = 1

SYSTEM_PROMPT = (
    "You are CreativePilot's brand analysis agent. You have tools to check "
    "memory, retrieve past brand-strategy context, and run the full brand "
    "analysis pipeline. For a brand analysis request, always call "
    "analyze_brand_tool to produce the structured profile -- you may first "
    "call retrieve_brand_context or retrieve_rag_context if it helps you "
    "choose better arguments (e.g. confirming tone). Once you have a "
    "structured brand profile, reply with ONLY that JSON object."
)


class AgentState(TypedDict):
    brand_input: dict
    messages: list
    result: Optional[dict]
    validated: bool
    retries: int
    error: Optional[str]


def analyze_request(state: AgentState) -> AgentState:
    brand_input = state["brand_input"]
    task = f"Analyze this brand and return its structured profile: {json.dumps(brand_input)}"
    state["messages"] = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=task)]
    state["retries"] = 0
    state["validated"] = False
    state["result"] = None
    state["error"] = None
    return state


def agent_node(state: AgentState) -> AgentState:
    llm = get_agent_llm().bind_tools(AGENT_TOOLS)
    response = llm.invoke(state["messages"])
    state["messages"] = state["messages"] + [response]
    return state


def route_after_agent(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    return "generate_response"


# handle_tool_errors=True: if a tool raises (e.g. Ollama down, RAG embed
# failure not already caught inside the tool), turn it into a ToolMessage
# the agent can see and react to, instead of crashing the whole graph.
tool_node = ToolNode(AGENT_TOOLS, handle_tool_errors=True)


# ============================================================================
# TEMPORARY DEBUG LOGGING -- remove once you've confirmed real Ollama tool
# calling is working end-to-end.
#
# Hooks LangChain's callback system around tool execution (fires for every
# tool call ToolNode makes) without touching ToolNode's registration or any
# graph node/edge. Passed into graph.invoke() via config in run_agent(), so
# the graph's structure above is completely unchanged.
# ============================================================================
class ToolCallDebugLogger(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        tool_name = serialized.get("name", "unknown_tool") if serialized else "unknown_tool"
        print(f"\n🔧 [TOOL CALL] name={tool_name}")
        print(f"    args: {input_str}")

    def on_tool_end(self, output, **kwargs):
        # `output` is sometimes the raw string, sometimes a ToolMessage --
        # print just the readable content either way.
        content = getattr(output, "content", output)
        print(f"✅ [TOOL RESULT] {content}")

    def on_tool_error(self, error, **kwargs):
        print(f"❌ [TOOL ERROR] {error!r}")
# ============================================================================
# END TEMPORARY DEBUG LOGGING
# ============================================================================


def generate_response(state: AgentState) -> AgentState:
    """Pull the structured profile out of the tool trail, or force one direct
    analyze_brand_tool call so the endpoint always returns a real result."""
    for message in reversed(state["messages"]):
        if isinstance(message, ToolMessage) and message.name == "analyze_brand_tool":
            try:
                state["result"] = json.loads(message.content)
            except (json.JSONDecodeError, TypeError):
                state["result"] = None
            break

    if state["result"] is None:
        try:
            raw = analyze_brand_tool.invoke(state["brand_input"])
            state["result"] = json.loads(raw)
        except Exception as e:
            state["error"] = str(e)
            state["result"] = None

    return state


def validate_output(state: AgentState) -> AgentState:
    if state["result"] is None:
        state["validated"] = False
        state["error"] = state["error"] or "No result produced by agent."
        return state

    try:
        BrandOutput(**state["result"])
        state["validated"] = True
    except Exception as e:
        state["validated"] = False
        state["error"] = str(e)

    return state


def route_after_validate(state: AgentState) -> str:
    if state["validated"]:
        return "end"
    if state["retries"] < MAX_RETRIES:
        return "retry"
    return "fallback"


def retry_node(state: AgentState) -> AgentState:
    state["retries"] += 1
    state["messages"] = state["messages"] + [
        HumanMessage(
            content=(
                f"Your last output failed validation: {state['error']}. "
                "Call analyze_brand_tool again and return only its JSON output."
            )
        )
    ]
    return state


def fallback_node(state: AgentState) -> AgentState:
    state["result"] = fallback_brand_profile()
    state["validated"] = True
    plural = "y" if state["retries"] == 1 else "ies"
    state["error"] = f"Fell back to safe defaults after {state['retries']} retr{plural}: {state['error']}"
    return state


def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("analyze_request", analyze_request)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.add_node("generate_response", generate_response)
    graph.add_node("validate", validate_output)
    graph.add_node("retry", retry_node)
    graph.add_node("fallback", fallback_node)

    graph.add_edge(START, "analyze_request")
    graph.add_edge("analyze_request", "agent")
    graph.add_conditional_edges(
        "agent", route_after_agent, {"tools": "tools", "generate_response": "generate_response"}
    )
    graph.add_edge("tools", "agent")
    graph.add_edge("generate_response", "validate")
    graph.add_conditional_edges(
        "validate", route_after_validate, {"end": END, "retry": "retry", "fallback": "fallback"}
    )
    graph.add_edge("retry", "agent")
    graph.add_edge("fallback", END)

    return graph.compile()


_agent_graph = None


def get_agent_graph():
    global _agent_graph
    if _agent_graph is None:
        _agent_graph = build_agent_graph()
    return _agent_graph


def run_agent(brand_input: dict) -> dict:
    """Entry point used by the new /agent/analyze-brand FastAPI route."""
    graph = get_agent_graph()
    # TEMPORARY: callbacks=[ToolCallDebugLogger()] prints tool name/args/result
    # to the terminal for every tool call. Remove this config once verified.
    final_state = graph.invoke(
        {"brand_input": brand_input},
        config={"callbacks": [ToolCallDebugLogger()]},
    )
    return {
        "result": final_state["result"],
        "validated": final_state["validated"],
        "error": final_state.get("error"),
        "retries": final_state["retries"],
    }
