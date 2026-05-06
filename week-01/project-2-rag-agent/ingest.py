"""
ingest.py — Chunk, embed, and store documents in ChromaDB.

Run this once before starting the RAG agent:
  python ingest.py

It reads all .txt files from the docs/ folder,
splits them into chunks, embeds them, and stores them locally.
"""

import os
import glob
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

DOCS_DIR = Path(__file__).parent / "docs"
CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "documents"

CHUNK_SIZE = 500       # characters per chunk
CHUNK_OVERLAP = 50     # overlap between chunks


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def ingest_documents():
    """Read all .txt files, chunk them, embed, and store in ChromaDB."""

    # Use sentence-transformers for local embedding (no API key needed)
    # Swap to OpenAI embeddings later if you want higher quality
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"   # Fast, free, good quality for starting out
    )

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Delete existing collection if re-ingesting
    try:
        client.delete_collection(COLLECTION_NAME)
        print("Deleted existing collection.")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )

    # Find all .txt files
    txt_files = glob.glob(str(DOCS_DIR / "*.txt"))
    if not txt_files:
        print(f"No .txt files found in {DOCS_DIR}")
        print("Add some .txt documents to the docs/ folder and run again.")
        return

    all_chunks = []
    all_ids = []
    all_metadata = []

    for filepath in txt_files:
        filename = Path(filepath).name
        print(f"Processing: {filename}")

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        print(f"  → {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            chunk_id = f"{filename}__chunk_{i}"
            all_chunks.append(chunk)
            all_ids.append(chunk_id)
            all_metadata.append({"source": filename, "chunk_index": i})

    # Store in ChromaDB (embeds automatically using the embedding function)
    collection.add(
        documents=all_chunks,
        ids=all_ids,
        metadatas=all_metadata
    )

    print(f"\n✓ Ingested {len(all_chunks)} chunks from {len(txt_files)} files.")
    print(f"  Stored in: {CHROMA_DIR}")


if __name__ == "__main__":
    ingest_documents()
