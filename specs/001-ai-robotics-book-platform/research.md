# Research for AI & Robotics Book Platform

## Decision: Technology Stack Selection
**Rationale**: The technology stack is predetermined by the project constitution and feature specification. We'll use Docusaurus for the frontend, deployed on GitHub Pages, with a backend using FastAPI, Neon Postgres, and Qdrant Cloud for the RAG functionality. This stack was chosen because it's explicitly required by the constitution and provides the necessary capabilities for our feature set.

**Alternatives considered**: 
- Next.js instead of Docusaurus: Rejected because the constitution mandates Docusaurus
- Different database: Rejected because the constitution mandates Neon Postgres
- Different vector database: Rejected because the constitution mandates Qdrant Cloud

## Decision: Authentication System
**Rationale**: Better-Auth was selected as the authentication system because it's required by the constitution. It provides the necessary capabilities for collecting user background information during signup and maintaining session management.

**Alternatives considered**:
- Auth0: Rejected because the constitution mandates Better-Auth
- Firebase Auth: Rejected because the constitution mandates Better-Auth
- Custom auth system: Rejected because the constitution mandates Better-Auth

## Decision: RAG Implementation Approach
**Rationale**: We'll use OpenAI Agents SDK with Qdrant Cloud for the RAG functionality. This will allow us to index the book content into vector embeddings and create an AI-powered chatbot that can answer questions based on the book content and user-selected text. This approach was chosen because it's required by the constitution and provides the necessary retrieval capabilities.

**Alternatives considered**:
- Using different LLM providers: Rejected because the constitution mandates OpenAI Agents SDK
- Different vector databases: Rejected because the constitution mandates Qdrant Cloud
- Different RAG frameworks: Rejected because the constitution mandates OpenAI Agents SDK

## Decision: Urdu Translation Implementation
**Rationale**: For Urdu translation, we'll implement a toggle system that switches between English and AI-generated but technically consistent Urdu translations. We'll use a combination of pre-translated content and potentially an API for dynamic translation as needed. This approach aligns with the requirement for AI-generated but technically consistent translations.

**Alternatives considered**:
- Manual translation only: Rejected because constitution specifies AI-generated translations
- Third-party translation service: Could consider this if pre-translated content isn't available
- Real-time translation API: Could be used as fallback, but pre-translation is preferred for consistency

## Decision: Content Generation Approach
**Rationale**: For content generation, we'll use Claude Code subagents as specified in the feature requirements. This approach will help ensure technical accuracy and consistency across the 11 book chapters. We'll develop templates and prompts that align with the academic and industry book structure requirement.

**Alternatives considered**:
- Manual writing only: Rejected because feature specifies Claude Code subagents
- Other AI writing tools: Rejected because feature specifies Claude Code subagents
- Mixed human/AI approach: Will likely be the practical approach, with Claude subagents generating drafts that humans review and refine