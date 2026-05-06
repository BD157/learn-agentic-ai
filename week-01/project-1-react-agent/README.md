# Project 1 — Manual ReAct Agent

**Concept:** Build the agent loop by hand. No LangChain. No LangGraph. Raw Anthropic API.

**Why:** You need to see every step before a framework hides it from you.

---

## What It Does

- Takes a user question
- Decides which tool to call (web search, calculator, or current time)
- Executes the tool
- Feeds the result back to Claude
- Loops until Claude has a final answer
- Prints the answer + full trace of every step taken

---

## How to Run

```bash
cd week-01/project-1-react-agent
python agent.py
```

You'll be prompted to enter a question. Try:
- `"What is 23% of 4,892?"`
- `"What day of the week is today, and what is today's date squared as a number?"`
- `"Search for the latest news about LangGraph and summarize it"`

---

## Files

```
project-1-react-agent/
├── README.md       ← you are here
├── agent.py        ← main agent loop
└── tools.py        ← tool definitions + execution
```

---

## Key Things to Understand

1. **The model never runs code.** It outputs a structured tool call. You catch it and run it.
2. **Tool results go back into the conversation as a new message.** That's how the model "sees" what happened.
3. **The loop runs until the model stops calling tools.** That's your signal it has the answer.
4. **`max_iterations` is your safety net.** Without it, a confused model loops forever.

---

## My Notes

*(Add your own observations here as you build)*

- What surprised me:
- What broke first:
- What I changed and why:
