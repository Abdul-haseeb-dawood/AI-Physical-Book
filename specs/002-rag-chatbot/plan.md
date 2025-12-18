# Implementation Plan: RAG Chatbot System

**Feature Branch**: `002-rag-chatbot`
**Created**: 2025-12-18
**Planner**: Qwen Code
**Reviewers**: Project Team
**Status**: Draft

## Technical Context

Provide technical context for the implementation:

- **Infrastructure**: Backend service using FastAPI with Qdrant vector database, integration with Docusaurus frontend, potentially Neon Postgres for chat history
- **Data flow**: Book content gets indexed as vector embeddings → user query → semantic search in Qdrant → context retrieved → OpenAI Agent generates response based on context → response sent to UI
- **Existing systems**: Integrates with Docusaurus book platform, uses OpenAI API, connects to Qdrant vector database, potentially Neon Postgres for chat history
- **Performance requirements**: Responses within 5 seconds (as per success criteria), handle 100 concurrent users, minimize latency for smooth user experience
- **Security considerations**: Rate limiting per IP, secure handling of API keys, environment-based secrets, protection against prompt injection attacks

## Constitution Check

Check against the project constitution:

- [x] Feature aligns with core principles (embedded RAG chatbot in book as required)
- [x] Uses required technology stack (FastAPI, OpenAI Agents SDK, Neon Postgres, Qdrant)
- [x] Follows development workflow requirements
- [x] Meets content standards (enables content-based Q&A)
- [x] Addresses governance requirements

### Gate Evaluation

All constitution principles are aligned with this implementation:
- Infrastructure choices: Using exactly the prescribed stack (FastAPI, OpenAI Agents, Neon Postgres, Qdrant)
- Technology choices: Aligned with approved technology stack from constitution
- Compliance: Fully compliant with all constitutional requirements

## Phase 0: Outline & Research

### Architecture Overview

- **Frontend Component**: Floating chat widget embedded in Docusaurus pages with text selection capability
- **Backend Service**: FastAPI application handling API requests, orchestrating the RAG flow
- **Vector Database**: Qdrant storing book content embeddings with metadata (chapter, section, page)
- **AI Processing**: OpenAI Agent using retrieved context to answer questions without hallucination
- **Data Flow**: Book MD → Embedding Pipeline → Qdrant Index → User Query → Semantic Search → Context Retrieval → AI Response

### Unknown Resolution

- [x] Content filtering strictness: System will acknowledge when it cannot answer from book content and inform the user
- [x] Embedding models: Research which embedding model works best for technical book content - Using OpenAI's text-embedding-3-small
- [x] Frontend integration: Research best practices for integrating floating widgets in Docusaurus - Using React component via custom plugin

## Phase 1: Design & Contracts

### Data Model

- **ChatMessage**: Contains user_id (optional), session_id, query_text, response_text, timestamp, source_context
- **BookChunk**: Contains content_id, chapter, section, page, content_text, embedding_vector, metadata
- **UserSession**: Contains session_id, user_id (optional), creation_timestamp, active_status
- **QueryContext**: Contains current_page, current_chapter, selected_text (if applicable), query_timestamp

### API Contracts

- **POST /chat**: Accepts query text, page context, and selected text; returns AI response based on book content
- **POST /chat/selected-text**: Accepts query and specific text selection; returns response focused on that text
- Request schema: {query: str, page?: str, chapter?: str, selected_text?: str}
- Response schema: {response: str, sources: [{content_id: str, chapter: str, section: str}], confidence: float}

### Component Design

- **EmbeddingPipeline**: Processes book markdown files into vector embeddings
- **RetrievalService**: Queries Qdrant for relevant content based on user query and context
- **OpenAIAgent**: Processes user query with retrieved context to generate response
- **RateLimiter**: Implements rate limiting to prevent system abuse
- **ChatController**: Orchestrates the entire flow from request to response

## Phase 2: Implementation Tasks

### Sprint 1: Foundation

- [ ] Set up FastAPI project with environment variable configuration
- [ ] Configure Qdrant client and create initial schema for book content
- [ ] Set up basic API endpoints (/chat, /chat/selected-text)

### Sprint 2: Core Feature

- [ ] Implement embedding pipeline to index book content into Qdrant
- [ ] Develop retrieval logic with chapter/context filtering
- [ ] Integrate OpenAI Agent with RAG to enforce book-only responses
- [ ] Implement rate limiting and security measures

### Sprint 3: Frontend Integration

- [ ] Build floating chat widget component for Docusaurus
- [ ] Implement text selection and query functionality
- [ ] Add loading and error states to UI
- [ ] Connect frontend to backend API

### Sprint 4: Testing & Quality Assurance

- [ ] Test for hallucination prevention (ensuring answers only from book content)
- [ ] Verify correct fallback messages when content isn't available
- [ ] Performance testing to meet 5-second response time requirement
- [ ] Security testing for prompt injection vulnerabilities

## Risks & Mitigations

- **Large book content**: Risk that indexing will take too long or cost too much. Mitigation: Chunk content sensibly and consider tiered approach for different book sections.
- **AI hallucination**: Risk that the AI generates responses not based on book content. Mitigation: Carefully craft prompts to emphasize using only provided context and include validation steps.
- **Performance under load**: Risk response times will exceed 5 seconds with many concurrent users. Mitigation: Implement caching, optimize queries, and add proper infrastructure monitoring.

## Success Criteria

How we'll verify the implementation matches the specification:

- [ ] Responses delivered within 5 seconds of user query
- [ ] At least 90% of responses accurately reference book content
- [ ] System functions with 100 concurrent users without degradation
- [ ] Users report improved understanding of book content
- [ ] Rate limiting successfully prevents abuse while allowing legitimate usage

## Dependencies

- [ ] Qdrant cloud instance access
- [ ] OpenAI API access with appropriate rate limits
- [ ] Access to book content in markdown format
- [ ] Docusaurus site structure understanding for frontend integration
