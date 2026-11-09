"""Workflow advisor MCP server: deterministic tools, no inner LLM, no API keys.

The host (Claude, ChatGPT, Cursor) is the model. It reads the user's message,
decides which tool to call, searches the web with its own search, and writes the
plan. This server supplies the two things a model should not improvise:
the method to follow, and exact arithmetic.

Local:   python server.py        (serves http://localhost:8000/mcp)
Inspect: fastmcp dev server.py
Cloud:   entrypoint  server.py:mcp
"""
import os

from fastmcp import FastMCP

GUIDE = """\
How to diagnose a repetitive workflow

1. Restate the workflow as steps. For each step name the input, the action and
   the output.
2. Collect the numbers. You need minutes per day and days per week. If the user
   has not given them, ask. Never assume values.
3. Look up current tools. Use web search so every tool you name exists today.
   If you cannot search, say the tool names are unverified.
4. Call estimate_time_saved with the numbers. Never do that arithmetic yourself.
5. Mark each step: automate now, automate with a human check, or keep manual.
   If you cannot describe a step precisely, do not automate it yet.

Reply with:
- One-line diagnosis
- A numbered automation plan (each step names a current tool and why)
- Hours saved per year (from the tool)
- One thing the user should verify before building
"""

mcp = FastMCP(
    "workflow-advisor",
    instructions=(
        "Use for anyone describing a repetitive process they want to automate. "
        "Call get_diagnosis_framework first and follow it. Call estimate_time_saved "
        "for any time-cost or hours-saved question."
    ),
)


@mcp.tool
def get_diagnosis_framework() -> str:
    """Return the method for diagnosing a messy, repetitive workflow and turning
    it into an automation plan. Call this FIRST whenever a user describes a
    process they want to improve or automate, then follow it step by step."""
    return GUIDE


@mcp.tool
def estimate_time_saved(minutes_per_day: float, days_per_week: int) -> dict:
    """Convert a task's minutes per day and days per week into hours lost per
    year. Use for any time-cost or hours-saved question. If the user has not
    given both numbers, ask for them first."""
    if minutes_per_day <= 0 or not 1 <= days_per_week <= 7:
        return {"error": "minutes_per_day must be > 0 and days_per_week between 1 and 7"}
    return {"hours_per_year": round(minutes_per_day * days_per_week * 52 / 60, 1)}


@mcp.prompt
def diagnose_my_workflow(workflow_description: str) -> str:
    """Start a workflow diagnosis from a description of the process."""
    return f"{GUIDE}\nWorkflow to diagnose:\n{workflow_description}"


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))