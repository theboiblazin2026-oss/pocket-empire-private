import chromadb
import ollama
import sys

# CONFIGURATION
COLLECTION_NAME = "legal_docs"

query = sys.argv[1] if len(sys.argv) > 1 else "What are the laws?"

from chromadb.config import Settings

# ...

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# Embed the query
try:
    response = ollama.embeddings(model="nomic-embed-text", prompt=query)
    query_embedding = response["embedding"]
except Exception as e:
    print(f"❌ Ollama Error: {e}")
    sys.exit(1)

# Query the DB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print(f"\n🔎 **Answer based on {COLLECTION_NAME}:**\n")
if results["documents"]:
    for i, doc in enumerate(results["documents"][0]):
        source = results["metadatas"][0][i]["source"]
        print(f"--- From {source} ---")
        print(doc)
        print("\n")
else:
    print("No results found.")
