# Project 1 — Manual ReAct Agent

This is a playful do-it-yourself thinking machine. It’s not a lecture, it’s a live experiment where the agent decides what to do next and you get to watch it in action.

**What happens here**

- You ask a question.
- The agent chooses whether to use a search, a calculator, or the current time.
- The code runs that tool and sends the result back.
- The agent keeps going until it has a complete answer.
- You see the full trail of decisions it made.

---

## Jump in and try it

From the project folder, run this command and then ask something curious:

```bash
cd week-01/project-1-react-agent
python agent.py
```

Here are some playful prompts to start with:
- What is 23% of 4,892?
- What day of the week is today, and what is today's date squared as a number?
- Search for the latest news about LangGraph and tell me what changed.

---

## Why this is fun

This is a taste of what agentic AI feels like:

- The model doesn’t execute code directly.
- It asks for tools, which your code runs.
- Results come back into the conversation like a teammate reporting what it found.
- The loop ends when the agent decides it has the answer.

---

## What’s in this folder

```
project-1-react-agent/
├── README.md       ← you are here
├── agent.py        ← main agent loop
└── tools.py        ← tool definitions + execution
```

---

## Handy notes

- The model outputs structured tool calls, not raw code.
- Your code catches the tool request and executes it.
- That execution result is sent back as a new message.
- `max_iterations` keeps the loop from running away.

---

## My Notes

*(Write down what surprised you, what broke, and what you changed.)*

- What surprised me:
- What broke first:
- What I changed and why:
