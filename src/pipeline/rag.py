import json
import chromadb
import os

# Initialize an in-memory Chroma client
chroma_client = chromadb.Client()

# Create or get a collection for the knowledge base
collection = chroma_client.create_collection(name="knowledge_base")

# Load the knowledge base dataset
current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, "..", "data", "knowledge_base.json")

with open(data_path, "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# Add documents to the ChromaDB collection
documents = []
metadatas = []
ids = []

for doc in knowledge_base:
    documents.append(doc["content"])
    metadatas.append({"title": doc["title"], "intent": doc["intent"]})
    ids.append(doc["id"])

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

def retrieve_knowledge(intent: str, top_k: int = 1) -> dict:
    """
    Retrieves the most relevant knowledge article for the given intent.
    Instead of using standard embedding search here, we can filter by the predicted intent metadata.
    """
    results = collection.get(
        where={"intent": intent},
        limit=top_k
    )
    
    # If no document found by exact intent, fallback to a general search (not implemented for simplicity)
    if not results['documents']:
        return None
        
    return {
        "title": results['metadatas'][0]["title"],
        "content": results['documents'][0]
    }
