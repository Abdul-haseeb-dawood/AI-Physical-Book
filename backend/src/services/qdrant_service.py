from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import os
from typing import List, Dict, Any

class QdrantManager:
    def __init__(self):
        # Initialize Qdrant client with environment variables
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            prefer_grpc=True
        )
        self.collection_name = "book_chapters"
        self.vector_size = 1536  # Default size for OpenAI ada-002 embeddings
        
    def setup_collection(self):
        """
        Create the collection for storing book chapter embeddings if it doesn't exist
        """
        # Check if collection exists
        collections = self.client.get_collections()
        collection_names = [col.name for col in collections.collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )
    
    def add_embeddings(self, chapter_id: str, embeddings: List[float], payload: Dict[str, Any]):
        """
        Add chapter embeddings to the collection
        """
        point = PointStruct(
            id=chapter_id,
            vector=embeddings,
            payload=payload
        )
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
    
    def search_similar(self, query_embedding: List[float], limit: int = 5):
        """
        Search for similar chapters based on embeddings
        """
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )
        return results