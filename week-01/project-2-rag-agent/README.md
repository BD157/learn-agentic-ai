# Project 2 — RAG Agent

**Concept:** Give the agent a document corpus. Before answering, it retrieves relevant chunks and grounds its response in real content.

**Builds on:** Project 1 — same agent loop, one new tool added: `retrieve_from_docs`.

---

## What It Does

1. Ingests a folder of `.txt` files → chunks → embeds → stores in ChromaDB
2. Agent has access to `retrieve_from_docs` tool
3. When a question is asked, agent retrieves relevant chunks before answering
4. Answer is grounded in your documents — no hallucination

---

## How to Run

**Step 1: Add your documents**
```bash
# Drop .txt files into the docs/ folder
cp your-documents/*.txt week-01/project-2-rag-agent/docs/
```

**Step 2: Ingest documents (run once)**
```bash
cd week-01/project-2-rag-agent
python ingest.py
```

**Step 3: Run the agent**
```bash
python agent.py
```

---

## Files

```
project-2-rag-agent/
├── README.md       ← you are here
├── ingest.py       ← chunks + embeds docs into ChromaDB
├── agent.py        ← RAG agent loop
├── tools.py        ← includes retrieve_from_docs tool
└── docs/           ← put your .txt files here
    └── .gitkeep
```

---

## Key Concepts

**Chunking:** Split documents into overlapping segments (~500 chars with 50 char overlap). Small enough to be specific, large enough to have context.

**Embedding:** Convert each chunk to a vector (a list of numbers). Similar content has similar vectors.

**Retrieval:** When a question comes in, embed the question, find the closest chunks by vector similarity. Those are your context.

**Grounding:** Pass retrieved chunks to the agent as tool output. Claude reads them before answering.

---

## My Notes

*(Add your own observations here as you build)*

- What documents did I use:
- What retrieval quality looked like:
- What I'd change:
