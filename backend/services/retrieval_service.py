from typing import List, Dict, Any, Optional
from services.embedding_service import EmbeddingService
from services.vector_db import VectorDBService
from config.settings import settings


class RetrievalService:
    """
    Service to handle retrieval of relevant content using vector search
    """
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_db = VectorDBService(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            collection_name=settings.QDRANT_COLLECTION_NAME
        )
    
    def retrieve_by_context(
        self, 
        query: str, 
        chapter_filter: Optional[str] = None, 
        section_filter: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant content based on query and context filters
        """
        # Generate embedding for the query
        query_embedding = self.embedding_service.generate_embedding(query)
        if not query_embedding:
            return []
        
        # Search in vector database with filters
        results = self.vector_db.search_by_text(
            query_vector=query_embedding,
            chapter_filter=chapter_filter,
            section_filter=section_filter,
            limit=limit
        )
        
        return results
    
    def retrieve_by_selected_text(
        self, 
        query: str, 
        selected_text: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve content specifically related to the selected text
        """
        # Generate embedding for the selected text
        selected_text_embedding = self.embedding_service.generate_embedding(selected_text)
        if not selected_text_embedding:
            return []
        
        # Search in vector database for content related to selected text
        results = self.vector_db.search_by_selected_text(
            query_vector=selected_text_embedding,
            selected_text=selected_text,
            limit=limit
        )
        
        return results
    
    def retrieve_general(
        self, 
        query: str, 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant content without specific filters
        """
        # Generate embedding for the query
        query_embedding = self.embedding_service.generate_embedding(query)
        if not query_embedding:
            return []
        
        # Search in vector database without filters
        results = self.vector_db.search_by_text(
            query_vector=query_embedding,
            limit=limit
        )
        
        return results