# learn-agentic-ai

A structured, hands-on learning journey through agentic AI — from a working ReAct agent to a production-grade multi-agent system.

> **Bias:** practical implementation over theory. Every week ends with something running.

---

## Structure

```
learn-agentic-ai/
├── week-01/        # Manual ReAct agent + RAG agent + data normalizer (no framework)
├── week-02/        # RAG agent + intro to LangGraph
├── week-03/        # LangGraph state machine + multi-tool agent
├── week-04/        # Observability + evals
├── month-02/       # Multi-agent, human-in-the-loop, production patterns
├── month-03/       # Production service, deployment, monitoring
└── notes/          # Concepts, resources, running log
```

---

## Progress Tracker

### 🔴 Week 1–2 — Foundation
- [ ] Python env configured (3.10+)
- [ ] API keys working (Anthropic + OpenAI)
- [ ] `.env` + `python-dotenv` set up
- [ ] Understand: agent loop, tool schemas, context window, ReAct pattern
- [ ] **Project 1:** Manual ReAct agent (no framework) ✦ working demo
- [ ] **Project 2:** RAG agent with ChromaDB ✦ working demo
- [ ] **Project 3:** Data normalizer agent ✦ working demo

### 🟡 Week 3–4 — LangGraph + Observability
- [ ] LangGraph installed, ReAct agent rebuilt with state machine
- [ ] Pydantic validation on all tool inputs/outputs
- [ ] Langfuse running, every LLM call logged
- [ ] Eval suite: 20 input/output pairs, pass rate tracked
- [ ] **Project 3:** Multi-tool agent with structured output ✦ working demo

### 🟠 Month 2 — Multi-Agent + Production Patterns
- [ ] **Project 4:** Multi-agent pipeline (Researcher + Writer)
- [ ] **Project 5:** Human-in-the-loop with approval gates
- [ ] Retry logic + exponential backoff on all LLM calls
- [ ] Cost tracking per run
- [ ] Context compression for long-running agents
- [ ] Hard limits: max tokens, iterations, wall-clock time

### 🟢 Month 3 — Production
- [ ] **Project 6:** Full eval suite (unit + trajectory + LLM-as-judge)
- [ ] **Project 7:** FastAPI service + Celery + Redis job queue
- [ ] Docker containerization
- [ ] Deployed + live monitoring dashboard
- [ ] MCP (Model Context Protocol) integration
- [ ] Cheap model routing (Haiku/mini for simple steps)

---

## Reading List (in order)

| Resource | When | Status |
|---|---|---|
| Anthropic Agent Cookbook — `docs.anthropic.com` | Week 1 | [ ] |
| "Building Effective Agents" — Anthropic blog | End of Week 2 | [ ] |
| LangGraph tutorials: ReAct → Human-in-Loop → Multi-Agent | Week 3 | [ ] |
| Chip Huyen — AI Engineering posts `huyenchip.com` | Month 2 | [ ] |
| "Patterns for Building LLM Systems" — Eugene Yan | Month 2 | [ ] |
| Simon Willison — `simonwillison.net` AI tag | Ongoing | [ ] |

---

## Ground Rules

1. Don't move to the next week until you have a working demo from the current one
2. Log every session in `notes/log.md`
3. Every agent project gets its own folder with a `README.md` and working code
4. Evals are not optional — write them before you touch the prompt
