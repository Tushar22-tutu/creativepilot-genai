"""
Small FastMCP server exposing CreativePilot's existing brand-intelligence
functions as MCP tools. This is a SEPARATE process from the FastAPI app in
backend/main.py -- it does not replace or duplicate it, it just exposes the
same underlying functions over MCP for any MCP-compatible client.

Run it standalone:

    python -m backend.mcp_server
"""

from fastmcp import FastMCP

from backend.brand_intelligence.analyzer import analyze_brand as _analyze_brand
from backend.brand_intelligence.memory import (
    get_brand_from_memory,
    load_memory_from_file,
    save_brand_to_memory,
)

mcp = FastMCP("CreativePilot")

load_memory_from_file()


@mcp.tool()
def get_brand_context(brand_name: str) -> dict:
    """Return a previously stored brand profile from persistent memory, if one exists."""
    cached = get_brand_from_memory(brand_name)
    return cached or {"found": False}


@mcp.tool()
def analyze_brand(
    brand_name: str,
    product: str = "",
    target_audience: str = "",
    tone: str = "professional",
) -> dict:
    """Run CreativePilot's existing brand analysis pipeline and return the structured profile."""
    return _analyze_brand(
        {
            "brand_name": brand_name,
            "product": product,
            "target_audience": target_audience,
            "tone": tone,
        }
    )


@mcp.tool()
def save_brand_memory(brand_name: str, brand_profile: dict) -> str:
    """Persist a brand profile to memory."""
    save_brand_to_memory(brand_name, brand_profile)
    return f"Saved profile for '{brand_name}'."


if __name__ == "__main__":
    mcp.run()
