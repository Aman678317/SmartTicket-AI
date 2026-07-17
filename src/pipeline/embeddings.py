from sentence_transformers import SentenceTransformer

# Load a small, fast model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> list[float]:
    """
    Converts text to a vector embedding.
    Returns a list of floats representing the embedding vector.
    """
    embedding = model.encode(text)
    return embedding.tolist()
