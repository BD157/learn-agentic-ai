# Week 1 — The Agent Loop

**Goal:** Have two working agents by Friday. No frameworks. Raw API only.

---

## What You're Building

| Project | What It Does | New Concept |
|---|---|---|
| Project 1 | ReAct agent with 3 tools, answers multi-step questions | Agent loop, tool schemas, tool execution |
| Project 2 | RAG agent that reads a document corpus before answering | Chunking, embeddings, vector retrieval |

---

## Day-by-Day Plan

### Day 1 — Environment + First LLM Call
- [ ] Python 3.10+ virtual environment created
  ```bash
  python -m venv .venv
  source .venv/bin/activate        # Mac/Linux
  .venv\Scripts\activate           # Windows
  pip install -r requirements.txt
  ```
- [ ] `.env` file created from `.env.example`, keys filled in
- [ ] Run a raw API call — just get a response back from Claude
- [ ] Read: [Anthropic tool use docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

### Day 2 — Tools
- [ ] Write 3 tools: `search_web`, `calculate`, `get_current_time`
- [ ] Write the tool schema for each (name, description, parameters)
- [ ] Call Claude with tools defined — see it choose one
- [ ] Execute the tool manually, print the result

### Day 3 — The Loop
- [ ] Build the full ReAct loop: Think → Act → Observe → Repeat
- [ ] Feed tool results back into conversation history
- [ ] Add exit condition: model stops calling tools when it has the answer
- [ ] Add max iterations guard (fail after 10 steps)

### Day 4 — Test + Polish Project 1
- [ ] Test with 5 different multi-step questions
- [ ] Log every step to terminal (which tool, what args, what result)
- [ ] Write `week-01/project-1-react-agent/README.md` — what it does, how to run it
- [ ] **Demo:** Ask "What is 15% of the current year, and what day of the week is it today?" — agent should use calculate + time tools

### Day 5 — Project 2: RAG Agent
- [ ] Install ChromaDB, set up local collection
- [ ] Chunk 3–5 text files (any docs you care about)
- [ ] Embed chunks + store in Chroma
- [ ] Add `retrieve_from_docs` as a tool in your agent
- [ ] **Demo:** Ask a question only answerable from your documents — agent retrieves and answers correctly

---

## Concepts to Internalize This Week

### The Agent Loop
```
User Input
    │
    ▼
┌─────────────────────────────────┐
│  LLM thinks:                    │
│  "I need to call [tool]         │
│   with [arguments]"             │
└────────────┬────────────────────┘
             │ tool call
             ▼
┌─────────────────────────────────┐
│  Your code executes the tool    │
│  Returns result to LLM          │
└────────────┬────────────────────┘
             │ observe result
             ▼
┌─────────────────────────────────┐
│  LLM thinks again:              │
│  "Do I have the answer?         │
│   Or do I need another tool?"   │
└────────────┬────────────────────┘
             │
        ┌────┴────┐
        │         │
      Done     Loop again
```

### Tool Schema Anatomy
```python
tool = {
    "name": "calculate",
    "description": "Evaluate a math expression and return the result. Use for any arithmetic.",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "A valid Python math expression e.g. '(15 / 100) * 2024'"
            }
        },
        "required": ["expression"]
    }
}
```
**Key:** The description is for the model, not for you. Write it so the model knows *when* to use this tool and *what to pass in*.

### Context Window as RAM
- Everything the agent knows lives in the messages list
- Tool results are added as messages — the model reads them on the next step
- If you don't add it to messages, the agent doesn't know it happened

---

## Projects

- [`project-1-react-agent/`](./project-1-react-agent/) — Manual ReAct agent
- [`project-2-rag-agent/`](./project-2-rag-agent/) — RAG agent with ChromaDB

---

## Done When
- [ ] Project 1 answers a multi-step question using 2+ tools correctly
- [ ] Project 2 answers a question from your document corpus correctly
- [ ] You can explain the agent loop out loud without looking at notes
