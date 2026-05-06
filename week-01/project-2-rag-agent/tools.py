"""
tools.py — Tools for the RAG agent.

Extends Project 1 tools with: retrieve_from_docs
"""

import math
import datetime
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "documents"
N_RESULTS = 3   # number of chunks to retrieve per query


# ─────────────────────────────────────────────
# CHROMA CLIENT (lazy init)
# ─────────────────────────────────────────────

_collection = None

def get_collection():
    global _collection
    if _collection is None:
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _collection = client.get_collection(name=COLLECTION_NAME, embedding_function=ef)
    return _collection


# ─────────────────────────────────────────────
# TOOL SCHEMAS
# ─────────────────────────────────────────────

TOOL_SCHEMAS = [
    {
        "name": "retrieve_from_docs",
        "description": (
            "Search the document knowledge base and retrieve relevant passages. "
            "Use this FIRST when the user asks a question that might be answered by the documents. "
            "Returns the most relevant text chunks found."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A natural language query to search the documents with"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculate",
        "description": "Evaluate a mathematical expression. Use for any arithmetic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A valid Python math expression"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_current_datetime",
        "description": "Returns the current date and time.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]


# ─────────────────────────────────────────────
# TOOL EXECUTION
# ─────────────────────────────────────────────

def retrieve_from_docs(query: str) -> str:
    """Search ChromaDB for chunks relevant to the query."""
    try:
        collection = get_collection()
        results = collection.query(query_texts=[query], n_results=N_RESULTS)

        if not results["documents"] or not results["documents"][0]:
            return "No relevant documents found for this query."

        output_parts = []
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            source = meta.get("source", "unknown")
            output_parts.append(f"[Chunk {i+1} from '{source}']\n{doc}")

        return "\n\n---\n\n".join(output_parts)

    except Exception as e:
        return f"Retrieval error: {e}. Did you run ingest.py first?"


def calculate(expression: str) -> str:
    try:
        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"


def get_current_datetime() -> str:
    now = datetime.datetime.now()
    return f"Current datetime: {now.strftime('%A, %B %d, %Y at %I:%M %p')}"


# ─────────────────────────────────────────────
# DISPATCHER
# ─────────────────────────────────────────────

def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "retrieve_from_docs":
        return retrieve_from_docs(**tool_input)
    elif tool_name == "calculate":
        return calculate(**tool_input)
    elif tool_name == "get_current_datetime":
        return get_current_datetime()
    else:
        return f"Unknown tool: '{tool_name}'"
