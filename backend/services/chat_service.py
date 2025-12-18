from typing import Dict, List, Any
from models.query_context import QueryContext
from services.embedding_service import EmbeddingService
from services.retrieval_service import RetrievalService
from services.validation_service import ValidationService
from services.prompt_security import PromptSecurityService
from services.cache_service import CacheService
from services.session_service import SessionService
from utils.logger import logger
from utils.analytics import AnalyticsService
from config.settings import settings
from openai import OpenAI
import logging


class ChatService:
    """
    Service to process queries using RAG (Retrieval-Augmented Generation)
    """
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.retrieval_service = RetrievalService()
        self.validation_service = ValidationService()
        self.security_service = PromptSecurityService()
        self.cache_service = CacheService()
        self.session_service = SessionService()
        self.analytics_service = AnalyticsService()
        self.client = OpenAI(api_key=settings.GEMINI_API_KEY)

    def process_query(self, query: str, query_context: QueryContext, ip_address: str = None) -> Dict[str, Any]:
        """
        Process a user query using RAG approach
        """
        try:
            # Check cache first
            cache_context = f"{query_context.current_chapter or ''}:{query_context.selected_text or ''}"
            cached_result = self.cache_service.get(query, cache_context)
            if cached_result:
                logger.log_info(f"Cache hit for query: {query[:50]}...")
                # Still track the query for analytics, even if cached
                self.analytics_service.track_query(query, len(cached_result.get("response", "")), success=True)
                return cached_result

            # Validate the query
            if not self.validation_service.validate_query(query):
                self.analytics_service.track_query(query, 0, success=False)
                return {
                    "response": "Invalid query provided.",
                    "sources": [],
                    "confidence": 0.0
                }

            # Sanitize the query
            sanitized_query = self.validation_service.sanitize_input(query)

            # Check for prompt injection
            is_injected, injection_patterns = self.security_service.check_for_injection(sanitized_query)
            if is_injected:
                logger.log_security_event(
                    event_type="PROMPT_INJECTION_ATTEMPT",
                    details={"patterns": injection_patterns, "query": sanitized_query},
                    ip_address=ip_address
                )
                self.analytics_service.track_query(query, 0, success=False)
                return {
                    "response": "Your query contains content that appears to be attempting to manipulate the system. Please rephrase your question.",
                    "sources": [],
                    "confidence": 0.0
                }

            # Sanitize selected text if present
            selected_text = query_context.selected_text
            if selected_text:
                selected_text = self.validation_service.sanitize_input(selected_text)

                # Validate selected text
                if not self.validation_service.validate_selected_text(selected_text):
                    self.analytics_service.track_query(query, 0, success=False)
                    return {
                        "response": "Invalid selected text provided.",
                        "sources": [],
                        "confidence": 0.0
                    }

            # Search for relevant content in the vector database based on query and context
            search_results = []

            if selected_text:
                # If there's selected text, search specifically for content related to it
                search_results = self.retrieval_service.retrieve_by_selected_text(
                    query=sanitized_query,
                    selected_text=selected_text,
                    limit=5
                )
            else:
                # Otherwise, search with chapter context if available
                search_results = self.retrieval_service.retrieve_by_context(
                    query=sanitized_query,
                    chapter_filter=query_context.current_chapter,
                    limit=10
                )

            if not search_results:
                self.analytics_service.track_query(query, 0, success=True)  # Success in the sense that we handled it
                return {
                    "response": "I couldn't find relevant information in the book to answer your question.",
                    "sources": [],
                    "confidence": 0.0
                }

            # Build context from search results
            context_texts = [result["content_text"] for result in search_results]
            context = "\n\n".join(context_texts)

            # Verify context safety
            for context_text in context_texts:
                if not self.security_service.is_safe_context(context_text):
                    logger.log_security_event(
                        event_type="UNSAFE_CONTEXT_DETECTED",
                        details={"context": context_text},
                        ip_address=ip_address
                    )
                    continue  # Skip unsafe context but continue with safe ones

            # Sanitize query for context inclusion
            safe_query = self.security_service.sanitize_query_for_context(sanitized_query)

            # Create the message for the LLM
            messages = [
                {
                    "role": "system",
                    "content": f"You are an AI assistant for the 'Physical AI & Humanoid Robotics' book. "
                               f"Answer questions based ONLY on the provided book content. "
                               f"If the answer is not in the provided context, clearly state that you couldn't find the information. "
                               f"Be helpful and concise, and reference the book content when possible."
                },
                {
                    "role": "user",
                    "content": f"Context from the book:\n{context}\n\nQuestion: {safe_query}"
                }
            ]

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=settings.GPT_MODEL,
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent answers
                max_tokens=500
            )

            # Extract the response
            llm_response = response.choices[0].message.content

            # Calculate a basic confidence score based on how much context was used
            confidence = min(len(search_results) / 10.0, 1.0)  # Scale based on number of results, max 1.0

            # Cache the successful result (for simple queries, not those with selected text which are more specific)
            if not selected_text:  # Only cache general queries, not those based on specific selected text
                self.cache_service.set(
                    query=sanitized_query,
                    context=cache_context,
                    data={
                        "response": llm_response,
                        "sources": search_results,
                        "confidence": confidence
                    },
                    ttl=300  # Cache for 5 minutes
                )

            # Log the query for monitoring
            logger.log_query(sanitized_query, llm_response, ip_address=ip_address)

            # Track analytics
            self.analytics_service.track_query(sanitized_query, len(llm_response), success=True)

            return {
                "response": llm_response,
                "sources": search_results,
                "confidence": confidence
            }

        except Exception as e:
            logging.error(f"Error in ChatService.process_query: {str(e)}")
            logger.log_error(str(e), {"query": query, "context": query_context.dict()})
            self.analytics_service.track_error()
            return {
                "response": "Sorry, I encountered an issue processing your query. Please try again later.",
                "sources": [],
                "confidence": 0.0
            }