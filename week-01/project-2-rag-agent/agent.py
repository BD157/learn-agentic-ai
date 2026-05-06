"""
agent.py — RAG Agent (Project 2)

Same loop as Project 1 — one new tool: retrieve_from_docs.
The agent searches your document corpus before answering.

Run:
  python ingest.py    ← once, to load your docs
  python agent.py     ← then this
"""

import os
from dotenv import load_dotenv
import anthropic
from rich.console import Console
from rich.panel import Panel

from tools import TOOL_SCHEMAS, execute_tool

load_dotenv()

MODEL = "claude-3-5-haiku-20241022"
MAX_ITERATIONS = 10
MAX_TOKENS = 4096

SYSTEM_PROMPT = """You are a helpful assistant with access to a document knowledge base and tools.

When answering questions:
1. ALWAYS start by retrieving relevant information from the documents using retrieve_from_docs
2. Base your answer primarily on what you find in the documents
3. If the documents don't contain relevant information, say so clearly — don't make things up
4. Use the calculate tool for any math
5. Use get_current_datetime for date/time questions

Be specific about which document your information comes from."""

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
console = Console()


def run_agent(user_question: str) -> str:
    messages = [{"role": "user", "content": user_question}]

    console.print(Panel(f"[bold cyan]Question:[/bold cyan] {user_question}", expand=False))

    for iteration in range(1, MAX_ITERATIONS + 1):
        console.print(f"\n[dim]── Step {iteration} ──────────────────────────────[/dim]")

        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")),
                "No answer returned."
            )
            console.print(Panel(
                f"[bold green]Answer:[/bold green]\n\n{final_text}",
                border_style="green",
                expand=False
            ))
            return final_text

        if response.stop_reason != "tool_use":
            return f"Unexpected stop: {response.stop_reason}"

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            console.print(f"[yellow]🔧 Tool:[/yellow] [bold]{block.name}[/bold]")
            console.print(f"   [dim]Input: {block.input}[/dim]")

            result = execute_tool(block.name, block.input)

            console.print(f"   [green]Result:[/green] {result[:300]}{'...' if len(result) > 300 else ''}")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result
            })

        messages.append({"role": "user", "content": tool_results})

    return f"Stopped after {MAX_ITERATIONS} iterations."


def main():
    console.print(Panel(
        "[bold]RAG Agent — Week 1, Project 2[/bold]\n"
        "[dim]Retrieval-augmented generation over your document corpus.[/dim]\n\n"
        "Make sure you ran: [bold]python ingest.py[/bold] first.\n"
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
