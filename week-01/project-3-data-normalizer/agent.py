import argparse
import os
import json
from dotenv import load_dotenv
import anthropic
from rich.console import Console
from rich.panel import Panel

from tools import TOOL_SCHEMAS, execute_tool, load_csv

load_dotenv()

MODEL = "claude-3-5-sonnet-20241022"
MAX_ITERATIONS = 25
MAX_TOKENS = 4096

SYSTEM_PROMPT = """You are a data normalization assistant with access to tools.

Your task is to clean a loaded CSV dataset following these steps:
1. Profile the data for column naming problems, inconsistent values, bad formats, null markers, and duplicates.
2. Normalize column names to snake_case.
3. Normalize values according to column-specific rules.
4. Fix common formats like ISO dates, E.164 phone numbers, and consistent text casing.
5. Replace invalid null markers with proper null values.
6. Detect duplicate rows according to duplicate key rules.
7. Export the cleaned CSV and a JSON audit report summarizing every change.

Use the available tools to complete the job. If a tool can help, call it. Do not guess about data changes without using a tool.
"""

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
console = Console()


def run_agent(task_description: str) -> str:
    messages = [{"role": "user", "content": task_description}]
    console.print(
        Panel(f"[bold cyan]Task:[/bold cyan] {task_description}", expand=False)
    )

    for iteration in range(1, MAX_ITERATIONS + 1):
        console.print(
            f"\n[dim]── Step {iteration} ──────────────────────────────[/dim]"
        )

        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")),
                "No answer returned.",
            )
            console.print(
                Panel(
                    f"[bold green]Final Answer:[/bold green]\n\n{final_text}",
                    border_style="green",
                    expand=False,
                )
            )
            return final_text

        if response.stop_reason == "max_tokens":
            return "Error: hit token limit before finishing. Try a simpler task."

        if response.stop_reason != "tool_use":
            return f"Unexpected stop reason: {response.stop_reason}"

        messages.append({"role": "assistant", "content": response.content})
        tool_results = []

        for block in response.content:
            if block.type != "tool_use":
                continue

            tool_name = block.name
            tool_input = block.input
            tool_use_id = block.id

            console.print(f"[yellow]🔧 Tool:[/yellow] [bold]{tool_name}[/bold]")
            console.print(f"   [dim]Input: {tool_input}[/dim]")

            result = execute_tool(tool_name, tool_input)
            console.print(
                f"   [green]Result:[/green] {result[:300]}{'...' if len(result) > 300 else ''}"
            )

            tool_results.append(
                {"type": "tool_result", "tool_use_id": tool_use_id, "content": result}
            )

        messages.append({"role": "user", "content": tool_results})

    return f"Agent stopped after {MAX_ITERATIONS} iterations without a final answer."


def main():
    parser = argparse.ArgumentParser(description="Project 3: Data Normalizer")
    parser.add_argument("--input", required=False, help="Path to input CSV file")
    args = parser.parse_args()

    if not args.input:
        console.print(
            Panel(
                "[bold]Data Normalizer — Week 1, Project 3[/bold]\n"
                "[dim]Pass --input <file> to run the normalization agent.[/dim]\n\n"
                "Example: python agent.py --input sample_data/sample.csv",
                title="learn-agentic-ai",
                border_style="blue",
            )
        )
        return

    input_path = os.path.abspath(args.input)
    if not os.path.exists(input_path):
        console.print(f"[red]Error:[/red] Input file not found: {input_path}")
        return

    load_csv(input_path)

    task = (
        f"The dataset from {input_path} is loaded in memory. "
        "Profile the data, normalize the columns and values, fix formats, replace invalid null markers, detect duplicates, "
        "and export a cleaned CSV plus a JSON audit report. "
        "Use the tools provided to complete the task."
    )

    run_agent(task)


if __name__ == "__main__":
    main()
