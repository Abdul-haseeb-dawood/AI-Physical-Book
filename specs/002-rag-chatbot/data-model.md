# Data Model: RAG Chatbot System

## Entity Definitions

### ChatMessage
- **Fields**:
  - id: UUID (primary key)
  - session_id: UUID (foreign key to UserSession)
  - user_id: UUID (optional, foreign key to User, null for anonymous users)
  - query_text: String (the user's question)
  - response_text: String (the AI's response)
  - timestamp: DateTime (when the message was created)
  - source_context: JSON (metadata about which content was used to generate the response)
  - confidence_score: Float (confidence level of the response, 0.0-1.0)

### BookChunk
- **Fields**:
  - content_id: String (unique identifier for this chunk)
  - chapter: String (chapter title/identifier)
  - section: String (section within the chapter)
  - page: String (page reference if applicable)
  - content_text: String (the actual text content of this chunk)
  - embedding_vector: Array<Float> (vector representation of the content for semantic search)
  - metadata: JSON (additional metadata like creation date, source file, etc.)
  - created_at: DateTime (when this chunk was indexed)

### UserSession
- **Fields**:
  - session_id: UUID (primary key)
  - user_id: UUID (optional, foreign key to User, null for anonymous users)
  - created_timestamp: DateTime (when the session started)
  - last_activity: DateTime (when the last message was exchanged)
  - active_status: Boolean (whether the session is still active)

### QueryContext
- **Fields**:
  - query_context_id: UUID (primary key)
  - session_id: UUID (foreign key to UserSession)
  - current_page: String (the page where the query originated)
  - current_chapter: String (the chapter where the query originated)
  - selected_text: String (text selected by the user, if applicable)
  - query_timestamp: DateTime (when the query was made)
  - context_metadata: JSON (additional context information)

## Validation Rules

### ChatMessage
- query_text length must be between 1 and 2000 characters
- response_text length must be between 1 and 5000 characters
- confidence_score must be between 0.0 and 1.0

### BookChunk
- content_text length must be between 50 and 2000 characters (for optimal context window)
- embedding_vector must have the correct dimensions for the chosen embedding model
- chapter and section must not be empty

### UserSession
- active_status can only be changed by the system based on last_activity and timeout rules

### QueryContext
- selected_text, if present, must be a substring of the relevant BookChunk content
- current_chapter must be valid according to the book's chapter structure

## Relationships

- UserSession (1) : ChatMessage (Many) - A session contains multiple chat messages
- UserSession (1) : QueryContext (Many) - A session can have multiple query contexts
- QueryContext (Many) : BookChunk (Many) - A query context can reference multiple book chunks
- ChatMessage (1) : QueryContext (1) - Each message is associated with a specific query context

## State Transitions

### UserSession
- Active → Inactive: When last_activity exceeds timeout period (e.g., 30 minutes)
- Inactive → Active: When a new message is sent in the session