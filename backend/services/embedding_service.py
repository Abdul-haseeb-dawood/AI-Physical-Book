import os
from typing import List, Optional
from openai import OpenAI
from config.settings import settings


class EmbeddingService:
    """
    Service to generate embeddings using OpenAI API
    """
    def __init__(self):
        self.client = OpenAI(api_key=settings.GEMINI_API_KEY)
        self.model = settings.EMBEDDING_MODEL  # Default to text-embedding-3-small

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        """
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            if embedding:
                embeddings.append(embedding)
            else:
                # Add a zero vector if embedding generation fails
                embeddings.append([0.0] * 1536)  # Default to 1536 dimensions for text-embedding-3-small
                
        return embeddings