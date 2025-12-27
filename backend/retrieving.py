import cohere
from qdrant_client import QdrantClient

cohere_client = cohere.Client("lIktbQOgIJ8VjIysFxkM9Bv8AnArRjmh37JdfjEK")

qdrant = QdrantClient(
    url="https://2134dfd0-9e1d-4561-9378-a3b7eecdd74d.europe-west3-0.gcp.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwiZXhwIjoxNzc0NjAwMzQ0fQ.hl0p5I85HIFGqC0JZ0BBhu4KSGN0fqpNxrsgBbQkN8k" 
)

def get_embedding(text):
    """Get embedding vector from Cohere Embed v3"""
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",  # Use search_query for queries
        texts=[text],
    )
    return response.embeddings[0]  # Return the first embedding

def retrieve(query):
    embedding = get_embedding(query)
    result = qdrant.query_points(
        collection_name="physical-ai-book",
        query=embedding,
        limit=5
    )
    return [point.payload["text"] for point in result.points]

print(retrieve("What data do you have? "))