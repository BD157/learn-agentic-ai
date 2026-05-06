# Core Concepts

Running notes on agentic AI concepts — updated as I learn.

---

## The Agent Loop

```
User Input → [Think → Act → Observe] → [Think → Act → Observe] → ... → Answer
```

An agent is not a chatbot. It loops until it decides it has enough information to answer.

**Key:** The model never runs code. It *outputs* a structured tool call. My code executes it.

---

## Tool Schemas

A tool schema is a JSON description that tells the model:
- What the tool is called
- When to use it (description)
- What arguments to pass (parameters)

The description field is the most important part. Write it for the model, not for yourself.

```python
{
    "name": "tool_name",
    "description": "When and why to use this tool. What it returns.",
    "input_schema": {
        "type": "object",
        "properties": {
            "param_name": {
                "type": "string",
                "description": "What this parameter is and what to put in it"
            }
        },
        "required": ["param_name"]
    }
}
```

---

## Context Window as RAM

- Everything the agent knows = what's in the messages list
- Tool results must be appended to messages or the agent "forgets" they happened
- Context is finite — manage it like a resource
- When context fills up: summarize, compress, or drop old tool results

---

## Memory Types

| Type | What It Is | When to Use |
|---|---|---|
| In-context | In the current messages list | Default — always |
| External (RAG) | Retrieved from vector DB | When corpus is too big for context |
| Episodic | Summarized past sessions | Multi-session continuity |
| Procedural | System prompt | Permanent instructions |

---

## ReAct Pattern

**Re**ason + **Act** — the most common agent pattern.

1. Model reasons about what it needs
2. Model calls a tool
3. Tool result is observed
4. Model reasons again
5. Repeat until answer is found

**vs. Plan-then-Execute:**
- Generate full plan first, then execute each step
- Better for predictable, structured tasks
- Use when you need auditability

---

## Stop Reasons

When Claude responds, check `response.stop_reason`:

| Value | Meaning | What to do |
|---|---|---|
| `"end_turn"` | Final answer ready | Extract text, return to user |
| `"tool_use"` | Wants to call a tool | Execute tool, append result, loop |
| `"max_tokens"` | Hit token limit | Handle gracefully, fail clean |

---

## My Questions / Things to Look Up

*(Add as you go)*

-
-
-
