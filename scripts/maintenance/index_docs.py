import os
import chromadb
import ollama

# CONFIGURATION
DOCS_DIR = "/Volumes/CeeJay SSD/KnowledgeBase/Legal" # User's actual path
COLLECTION_NAME = "legal_docs"

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name=COLLECTION_NAME)

files_processed = 0

print(f"I am reading files from {DOCS_DIR}...")

if not os.path.exists(DOCS_DIR):
    print(f"ERROR: Directory {DOCS_DIR} does not exist!")
    exit(1)

for root, dirs, files in os.walk(DOCS_DIR):
    for file in files:
        if file.endswith(".md") or file.endswith(".txt"):
            path = os.path.join(root, file)
            try:
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
            except Exception as e:
                print(f"Failed to process {file}: {e}")

print(f"Done! Indexed {files_processed} files.")
