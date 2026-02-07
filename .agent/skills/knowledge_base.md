---
name: knowledge_base
description: A skill to index and search local knowledge bases using Vector Search.
---

# Knowledge Base Expert

This skill allows you to index local markdown/text files and perform semantic searches against them. It uses **Ollama** for embeddings and **ChromaDB** for storage.

## Capabilities
1.  **Index**: Read all `.md` files in a directory and save them to a vector database.
2.  **Search**: Query the database to find relevant snippets.

## Setup
Ensure dependencies are installed:
\`\`\`bash
pip3 install chromadb ollama
ollama pull nomic-embed-text
\`\`\`

## Usage

### 1. Indexing a Directory
Run this script to index a folder (e.g., `KnowledgeBase/Legal`):

\`\`\`python
# index_docs.py
import os
import chromadb
import ollama

# CONFIGURATION
DOCS_DIR = "/Volumes/CeeJay SSD/KnowledgeBase/Legal" # CHANGE THIS
COLLECTION_NAME = "legal_docs"

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name=COLLECTION_NAME)

files_processed = 0

print(f"I am reading files from {DOCS_DIR}...")

for root, dirs, files in os.walk(DOCS_DIR):
    for file in files:
        if file.endswith(".md") or file.endswith(".txt"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Split by paragraphs (double newline) to make chunks
            chunks = content.split("\n\n")
            
            for i, chunk in enumerate(chunks):
                if len(chunk.strip()) > 50: # Skip empty/tiny chunks
                    # Generate embedding using Ollama
                    response = ollama.embeddings(model="nomic-embed-text", prompt=chunk)
                    embedding = response["embedding"]
                    
                    collection.add(
                        ids=[f"{file}_{i}"],
                        embeddings=[embedding],
                        documents=[chunk],
                        metadatas=[{"source": file}]
                    )
            print(f"Indexed: {file}")
            files_processed += 1

print(f"Done! Indexed {files_processed} files.")
\`\`\`

### 2. Searching the Knowledge Base
Run this script to ask a question:

\`\`\`python
# search_docs.py
import chromadb
import ollama
import sys

# CONFIGURATION
COLLECTION_NAME = "legal_docs"

query = sys.argv[1] if len(sys.argv) > 1 else "What are the laws?"

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name=COLLECTION_NAME)

# Embed the query
response = ollama.embeddings(model="nomic-embed-text", prompt=query)
query_embedding = response["embedding"]

# Query the DB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print(f"\n🔎 **Answer based on {COLLECTION_NAME}:**\n")
for i, doc in enumerate(results["documents"][0]):
    source = results["metadatas"][0][i]["source"]
    print(f"--- From {source} ---")
    print(doc)
    print("\n")
\`\`\`
