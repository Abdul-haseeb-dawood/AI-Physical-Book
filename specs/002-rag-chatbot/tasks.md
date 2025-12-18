# Tasks: RAG Chatbot System

## Feature Overview

The RAG Chatbot System integrates an AI-powered chatbot directly into the book pages, allowing users to ask questions and receive answers based solely on the book content. The system includes context-aware responses, selected-text querying, and robust backend services.

## Phase 1: Setup

### Goal
Initialize the project structure and configure necessary dependencies.

### Tasks

- [X] T001 Create backend directory structure (models, services, api, utils)
- [X] T002 Set up Python virtual environment with FastAPI dependencies
- [X] T003 Configure project environment variables and secrets management
- [X] T004 Install and configure Qdrant client library
- [X] T005 Install and configure OpenAI SDK
- [X] T006 Set up frontend build system for Docusaurus integration
- [X] T007 Create initial configuration files for backend and frontend

## Phase 2: Foundational

### Goal
Implement core infrastructure components that are required by multiple user stories.

### Tasks

- [X] T008 Implement BookChunk model with validation rules in backend/models/book_chunk.py
- [X] T009 Implement ChatMessage model with validation rules in backend/models/chat_message.py
- [X] T010 Implement UserSession model with validation rules in backend/models/user_session.py
- [X] T011 Implement QueryContext model with validation rules in backend/models/query_context.py
- [X] T012 Configure Qdrant collection for book content chunks in backend/services/vector_db.py
- [X] T013 Implement embedding generation function using OpenAI's text-embedding-3-small in backend/services/embedding_service.py
- [X] T014 Set up rate limiting middleware in backend/middleware/rate_limit.py
- [X] T015 Create database connection utilities for Neon Postgres in backend/db/connection.py

## Phase 3: User Story 1 - Embedded Chat Interface (Priority: P1)

### Goal
Enable users to access an AI chatbot directly on book pages without leaving the content.

### Independent Test
Users can open the floating chat widget on any book page and submit a question, receiving a response relevant to the book content.

### Tasks

- [X] T016 [P] [US1] Create basic chat UI component with message history in frontend/src/components/ChatWidget/ChatWidget.jsx
- [X] T017 [P] [US1] Implement floating widget positioning and visibility toggle in frontend/src/components/ChatWidget/ChatWidget.jsx
- [X] T018 [P] [US1] Add chat input field with submission handling in frontend/src/components/ChatWidget/ChatInput.jsx
- [X] T019 [US1] Implement POST /chat endpoint to receive queries and return responses in backend/api/chat_routes.py
- [X] T020 [US1] Create ChatService to process queries and generate responses in backend/services/chat_service.py
- [X] T021 [US1] Connect frontend chat component to backend API in frontend/src/components/ChatWidget/ChatAPI.js
- [X] T022 [US1] Implement basic loading and error states in chat UI in frontend/src/components/ChatWidget/ChatWidget.jsx
- [X] T023 [US1] Test basic chat functionality with mock API responses

## Phase 4: User Story 2 - Context-Aware Responses (Priority: P1)

### Goal
Ensure the AI understands which chapter or section the user is in when formulating responses.

### Independent Test
Questions asked while on a specific chapter yield responses that reference or relate to that chapter's content.

### Tasks

- [X] T024 [P] [US2] Update UI to pass page/chapter context with queries in frontend/src/components/ChatWidget/ChatAPI.js
- [X] T025 [US2] Modify POST /chat endpoint to accept and use page/chapter context in backend/api/chat_routes.py
- [X] T026 [US2] Implement retrieval function that filters by chapter/section in backend/services/retrieval_service.py
- [X] T027 [US2] Update ChatService to use context-aware retrieval in backend/services/chat_service.py
- [X] T028 [US2] Test that responses consider chapter context when formulating answers
- [X] T029 [US2] Validate that context information is properly stored in QueryContext model

## Phase 5: User Story 3 - Selected Text Querying (Priority: P2)

### Goal
Allow users to highlight specific text and ask questions specifically about that text selection.

### Independent Test
Users can highlight text, initiate a query about it, and receive answers focused specifically on the selected content.

### Tasks

- [X] T030 [P] [US3] Implement text selection detection in frontend/src/components/ChatWidget/TextSelectionHandler.js
- [X] T031 [P] [US3] Add selected text UI with query button in frontend/src/components/ChatWidget/SelectedTextPanel.jsx
- [X] T032 [US3] Implement POST /chat/selected-text endpoint in backend/api/chat_routes.py
- [X] T033 [US3] Update retrieval logic to focus on selected text context in backend/services/retrieval_service.py
- [X] T034 [US3] Connect text selection to backend API calls in frontend/src/components/ChatWidget/ChatAPI.js
- [X] T035 [US3] Test that responses are constrained to selected text content
- [X] T036 [US3] Validate that selected text is properly stored in QueryContext model

## Phase 6: User Story 4 - Secure and Reliable Backend Service (Priority: P3)

### Goal
Implement security measures and reliability features to protect user data and ensure consistent responses.

### Independent Test
System implements rate limiting and secure handling of user queries without exposing sensitive information.

### Tasks

- [X] T037 [P] [US4] Implement rate limiting for API endpoints in backend/middleware/rate_limit.py
- [X] T038 [P] [US4] Add API key validation to endpoints in backend/middleware/api_key_auth.py
- [X] T039 [US4] Implement secure handling of API keys and secrets in backend/config/settings.py
- [X] T040 [US4] Add input validation and sanitization for user queries in backend/services/validation_service.py
- [X] T041 [US4] Implement logging for security monitoring in backend/utils/logger.py
- [X] T042 [US4] Add protection against prompt injection attacks in backend/services/prompt_security.py
- [X] T043 [US4] Test rate limiting functionality under various load conditions
- [X] T044 [US4] Verify that sensitive information is not inadvertently stored in chat history

## Phase 7: Testing & Quality Assurance

### Goal
Implement comprehensive testing to ensure the system works correctly and meets quality standards.

### Tasks

- [X] T045 [P] Create unit tests for all backend services in backend/tests/test_*.py
- [X] T046 [P] Create integration tests for API endpoints in backend/tests/test_api.py
- [ ] T047 [P] Create frontend component tests in frontend/src/components/ChatWidget/__tests__/*
- [X] T048 Test for hallucination prevention ensuring answers only come from book content
- [X] T049 Verify correct fallback messages when content isn't available
- [X] T050 Performance testing to meet 5-second response time requirement
- [X] T051 Security testing for prompt injection vulnerabilities
- [X] T052 End-to-end testing of all user scenarios

## Phase 8: Polish & Cross-Cutting Concerns

### Goal
Finalize implementation with quality improvements and cross-cutting features.

### Tasks

- [X] T053 Implement proper error handling and user-friendly error messages in UI
- [X] T054 Add cache layer to improve response performance in backend/services/cache_service.py
- [X] T055 Implement session management for anonymous users in backend/services/session_service.py
- [X] T056 Add analytics and usage tracking (without PII) in backend/utils/analytics.py
- [X] T057 Optimize embedding pipeline for large book content in backend/services/embedding_pipeline.py
- [X] T058 Add documentation for the API and developer setup in docs/
- [X] T059 Create Docusaurus plugin to integrate chat widget in plugins/docusaurus-plugin-chat/
- [X] T060 Perform final integration testing across all components

## Dependencies

- User Story 1 (Embedded Chat Interface) must be completed before User Story 2 (Context-Aware Responses) and User Story 3 (Selected Text Querying)
- User Story 2 and User Story 3 share the core retrieval system which is part of User Story 1's foundation
- User Story 4 (Security) has some independent tasks but also depends on the APIs established in previous stories
- Testing phase (Phase 7) depends on all previous phases being complete

## Parallel Execution Examples

- T016, T017, T018 can run in parallel as they work on different frontend components
- T024, T025 can run in parallel as they work on UI and backend separately for context feature
- T030, T031 can run in parallel as they work on different aspects of text selection
- T037, T038 can run in parallel as they implement different security aspects
- T045, T046, T047 can run in parallel as they create tests for different layers

## Implementation Strategy

1. **MVP Scope**: Complete Phase 1 (Setup), Phase 2 (Foundational), and Phase 3 (User Story 1) to have a working chat interface that responds to queries
2. **Incremental Delivery**: After each phase, validate that the implemented functionality works as expected before moving to the next
3. **Iterative Refinement**: After core functionality works, enhance with additional features from higher phases
4. **Quality Assurance**: Throughout the implementation, run tests to ensure each component works correctly