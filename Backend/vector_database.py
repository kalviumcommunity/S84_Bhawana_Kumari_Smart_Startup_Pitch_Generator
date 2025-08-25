import chromadb
from chromadb.utils import embedding_functions

# Initialize ChromaDB client (local)
client = chromadb.Client()

# Create a collection for your startup ideas
collection = client.create_collection(name="startup_ideas")

# Example: Add embeddings to the database
def add_idea_to_db(idea_id, idea_text, embedding):
    collection.add(
        ids=[idea_id],
        embeddings=[embedding],
        documents=[idea_text]
    )

# Example: Query similar ideas by embedding
def query_similar_ideas(query_embedding, n_results=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results

# Example usage
if __name__ == "__main__":
    # Dummy embedding (replace with your real embedding from embeddings.py)
    dummy_embedding = [0.1] * 384  # For sentence-transformers/all-MiniLM-L6-v2
    add_idea_to_db("idea1", "AI-powered app that connects farmers to restaurants.", dummy_embedding)
    # Query with the same dummy embedding
    results = query_similar_ideas(dummy_embedding)
    print("Query results:", results)