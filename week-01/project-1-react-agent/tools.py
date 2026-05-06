"""
tools.py — Tool definitions and execution for the ReAct agent.

Each tool has two parts:
  1. A schema dict (sent to Claude so it knows the tool exists)
  2. An execution function (called by your code when Claude chooses the tool)
"""

import math
import datetime


# ─────────────────────────────────────────────
# TOOL SCHEMAS  (what Claude sees)
# ─────────────────────────────────────────────

TOOL_SCHEMAS = [
    {
        "name": "calculate",
        "description": (
            "Evaluate a mathematical expression and return the numeric result. "
            "Use for any arithmetic, percentages, or math operations. "
            "Expression must be a valid Python math expression."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A valid Python math expression e.g. '(15 / 100) * 4892' or 'math.sqrt(144)'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_current_datetime",
        "description": (
            "Returns the current date and time. "
            "Use when the user asks about today's date, the current time, or the current year."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "search_web",
        "description": (
            "Search the web for current information on a topic. "
            "Use for news, recent events, facts you might not know, or anything requiring up-to-date information."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A clear, specific search query"
                }
            },
            "required": ["query"]
        }
    }
]


# ─────────────────────────────────────────────
# TOOL EXECUTION  (what your code runs)
# ─────────────────────────────────────────────

def calculate(expression: str) -> str:
    """Safely evaluate a math expression."""
    try:
        # Restrict to safe math operations
        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating expression '{expression}': {e}"


def get_current_datetime() -> str:
    """Return the current date and time."""
    now = datetime.datetime.now()
    return (
        f"Current datetime: {now.strftime('%A, %B %d, %Y at %I:%M %p')}\n"
        f"Year: {now.year} | Month: {now.month} | Day: {now.day} | "
        f"Day of week: {now.strftime('%A')}"
    )


def search_web(query: str) -> str:
    """
    Stub web search — replace with a real search API.

    Options to wire in:
      - Tavily API (easiest): https://tavily.com — free tier available
      - Brave Search API: https://brave.com/search/api/
      - SerpAPI: https://serpapi.com
    """
    # TODO: Replace this stub with a real search API call
    # Example with Tavily:
    #
    # from tavily import TavilyClient
    # client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    # results = client.search(query=query, max_results=3)
    # return "\n\n".join([r["content"] for r in results["results"]])

    return (
        f"[STUB] Web search for: '{query}'\n"
        f"Wire in a real search API (Tavily recommended) to get live results.\n"
        f"See tools.py → search_web() for instructions."
    )


# ─────────────────────────────────────────────
# DISPATCHER  (routes tool name → function)
# ─────────────────────────────────────────────

def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool by name and return the result as a string."""
    if tool_name == "calculate":
        return calculate(**tool_input)
    elif tool_name == "get_current_datetime":
        return get_current_datetime()
    elif tool_name == "search_web":
        return search_web(**tool_input)
    else:
        return f"Unknown tool: '{tool_name}'"
