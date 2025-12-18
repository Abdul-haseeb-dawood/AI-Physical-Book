import os
from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from models.book_chunk import BookChunk


class VectorDBService:
    """
    Service to handle vector database operations with Qdrant
    """
    def __init__(self, url: str, api_key: str, collection_name: str = "book_content"):
        self.client = QdrantClient(
            url=url,
            api_key=api_key,
            prefer_grpc=True
        )
        self.collection_name = collection_name
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self):
        """
        Create the collection if it doesn't exist
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),  # OpenAI embedding size
            )
            
            # Create payload index for efficient filtering
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="chapter",
                field_schema=models.PayloadSchemaType.KEYWORD
            )
            
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="section",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

    def store_chunks(self, chunks: List[BookChunk]) -> bool:
        """
        Store multiple book chunks in the vector database
        """
        points = []
        for chunk in chunks:
            points.append(models.PointStruct(
                id=chunk.content_id,
                vector=chunk.embedding_vector,
                payload={
                    "content_id": chunk.content_id,
                    "chapter": chunk.chapter,
                    "section": chunk.section,
                    "page": chunk.page,
                    "content_text": chunk.content_text,
                    "metadata": chunk.metadata
                }
            ))
        
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return True
        except Exception as e:
            print(f"Error storing chunks: {e}")
            return False

    def search_by_text(self, query_vector: List[float], limit: int = 10, 
                      chapter_filter: Optional[str] = None, section_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks based on query vector
        """
        filters = []
        
        if chapter_filter:
            filters.append(models.FieldCondition(
                key="chapter",
                match=models.MatchValue(value=chapter_filter)
            ))
        
        if section_filter:
            filters.append(models.FieldCondition(
                key="section",
                match=models.MatchValue(value=section_filter)
            ))
        
        search_filter = models.Filter(must=filters) if filters else None
        
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=search_filter,
                limit=limit
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "content_id": result.payload.get("content_id"),
                    "chapter": result.payload.get("chapter"),
                    "section": result.payload.get("section"),
                    "page": result.payload.get("page"),
                    "content_text": result.payload.get("content_text"),
                    "score": result.score
                })
                
            return formatted_results
        except Exception as e:
            print(f"Error searching: {e}")
            return []

    def search_by_selected_text(self, query_vector: List[float], selected_text: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for chunks specifically related to selected text
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="content_text",
                            match=models.MatchText(text=selected_text)
                        )
                    ]
                ),
                limit=limit
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "content_id": result.payload.get("content_id"),
                    "chapter": result.payload.get("chapter"),
                    "section": result.payload.get("section"),
                    "page": result.payload.get("page"),
                    "content_text": result.payload.get("content_text"),
                    "score": result.score
                })
                
            return formatted_results
        except Exception as e:
            print(f"Error searching by selected text: {e}")
            return []