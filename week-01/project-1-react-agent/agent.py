"""
agent.py — Manual ReAct Agent (no framework)

The full agent loop, written by hand:
  Think → Act → Observe → Think → Act → Observe → ... → Answer

Run:
  python agent.py
"""

import os
from dotenv import load_dotenv
import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from tools import TOOL_SCHEMAS, execute_tool

load_dotenv()

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

MODEL = "claude-3-5-haiku-20241022"   # Fast + cheap for learning. Swap to claude-3-5-sonnet for harder tasks.
MAX_ITERATIONS = 10                    # Safety limit — agent stops after this many tool calls
MAX_TOKENS = 4096

SYSTEM_PROMPT = """You are a helpful assistant with access to tools.
When answering questions:
1. Think about what information you need
2. Use tools to gather that information
3. Combine the results into a clear, accurate answer

Always use tools when you need current information or need to do calculations.
Never guess at numbers — use the calculate tool.
Never guess at today's date — use the get_current_datetime tool."""

# ─────────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────────

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
console = Console()


# ─────────────────────────────────────────────
# AGENT LOOP
# ─────────────────────────────────────────────

def run_agent(user_question: str) -> str:
    """
    The core ReAct loop.

    messages: the full conversation history.
    Each iteration, we send the full history to Claude.
    Claude either calls a tool (we execute it, append result, loop again)
    or gives a final text answer (we return it).
    """

    messages = [
        {"role": "user", "content": user_question}
    ]

    console.print(Panel(f"[bold cyan]Question:[/bold cyan] {user_question}", expand=False))

    for iteration in range(1, MAX_ITERATIONS + 1):
        console.print(f"\n[dim]── Step {iteration} ──────────────────────────────[/dim]")

        # Call Claude with the full conversation + tool schemas
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages
        )

        # ── Check stop reason ───────────────────
        # "end_turn"    → Claude is done, final answer in response
        # "tool_use"    → Claude wants to call a tool
        # "max_tokens"  → hit token limit (handle gracefully)

        if response.stop_reason == "end_turn":
            # Extract the final text answer
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")),
                "No answer returned."
            )
            console.print(Panel(
                f"[bold green]Final Answer:[/bold green]\n\n{final_text}",
                border_style="green",
                expand=False
            ))
            return final_text

        if response.stop_reason == "max_tokens":
            return "Error: hit token limit before completing. Try a simpler question."

        if response.stop_reason != "tool_use":
            return f"Unexpected stop reason: {response.stop_reason}"

        # ── Process tool calls ───────────────────
        # Claude may call multiple tools in one response — handle all of them

        # First, add Claude's response (including its tool calls) to history
        messages.append({"role": "assistant", "content": response.content})

        # Build the tool results list
        tool_results = []

        for block in response.content:
            if block.type != "tool_use":
                continue

            tool_name = block.name
            tool_input = block.input
            tool_use_id = block.id

            console.print(f"[yellow]🔧 Tool:[/yellow] [bold]{tool_name}[/bold]")
            console.print(f"   [dim]Input: {tool_input}[/dim]")

            # Execute the tool
            result = execute_tool(tool_name, tool_input)

            console.print(f"   [green]Result:[/green] {result[:200]}{'...' if len(result) > 200 else ''}")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use_id,
                "content": result
            })

        # Add all tool results to history as a single user message
        messages.append({"role": "user", "content": tool_results})

    # If we hit max iterations without a final answer
    return f"Agent stopped after {MAX_ITERATIONS} iterations without a final answer. Try rephrasing your question."


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    console.print(Panel(
        "[bold]ReAct Agent — Week 1, Project 1[/bold]\n"
        "[dim]Manual agent loop. No framework. Raw Anthropic API.[/dim]\n\n"
        "Try: 'What is 23% of 4,892?'\n"
        "Try: 'What day of the week is today and what year is it?'\n"
        "Type 'exit' to quit.",
        title="learn-agentic-ai",
        border_style="blue"
    ))

    while True:
        question = input("\n> ").strip()
        if question.lower() in ("exit", "quit", "q"):
            break
        if not question:
            continue
        run_agent(question)


if __name__ == "__main__":
    main()
