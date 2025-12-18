# Research Findings: RAG Chatbot System

## Decision: Embedding Model Selection
**Rationale**: After researching various embedding models for technical content, OpenAI's text-embedding-3-small model was chosen because it offers a good balance of accuracy and cost-effectiveness for semantic search. It has 1536 dimensions which is sufficient for capturing the semantics of technical book content.

**Alternatives considered**:
- Sentence Transformers (all-MiniLM-L6-v2): Free option but less accurate for complex technical content
- Cohere embeddings: Good for technical content but requires additional API key management
- text-embedding-3-large: More accurate but significantly more expensive

## Decision: Docusaurus Widget Integration Approach
**Rationale**: Using a React-based floating widget component that gets injected into Docusaurus pages via a custom plugin. This approach allows for rich interactivity and seamless integration with the book content while maintaining Docusaurus's build process.

**Implementation approach**: 
1. Create a custom Docusaurus plugin that injects the chat widget component
2. Use React Context to manage state between the widget and page content
3. Implement text selection API to allow users to query specific text

**Alternatives considered**:
- Iframe integration: Simpler but limits interactivity with page content
- Pure JavaScript widget: Would require maintaining separate JS bundle
- Native Docusaurus theme component: More tightly integrated but harder to maintain separately

## Decision: Content Filtering Strictness
**Rationale**: The system will acknowledge when it cannot answer from book content and inform the user. This approach maintains user trust and clearly sets expectations about the system's capabilities while still being helpful.

**Implementation**:
- If retrieval doesn't find relevant content (below confidence threshold), the system responds with: "I couldn't find relevant information in the book to answer your question."
- The OpenAI agent is prompted to only use provided context and explicitly state when the context is insufficient.