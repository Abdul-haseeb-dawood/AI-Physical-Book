<!-- 
Sync Impact Report:
- Version change: 0.1.0 -> 1.0.0
- Modified principles: All principles replaced with AI Book project-specific content
- Added sections: Technical Stack, Development Workflow, Content Standards
- Removed sections: None
- Templates requiring updates: N/A (this is the first version)
- Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Book Constitution

## Core Principles

### Book Title & Platform
The book title is **"Physical AI & Humanoid Robotics"** and must be written using **Docusaurus** and deployed on **GitHub Pages**.

### Content Quality Standards
Content must be technically accurate, beginner to advanced friendly, and structured like a real academic + industry book with rigorous peer review processes.

### Personalization & Localization Features  
All chapters must support personalization for logged-in users and include an Urdu translation toggle to make the content accessible to a wider audience.

### Premium UI/UX Experience
UI must be premium/VIP quality with interactive, modern, dark-mode friendly design featuring smooth animations and readable typography for optimal learning experience.

### Integrated RAG Chatbot
A RAG chatbot must be embedded inside the book that answers ONLY from book content and can answer based on user-selected text to enhance the learning experience.

### Fixed Backend Technology Stack
Backend stack is fixed to FastAPI, OpenAI Agents/ChatKit SDK, Neon Serverless Postgres, and Qdrant Cloud (Free Tier) to ensure consistency and maintainability.

### User Authentication & Profiling
Authentication must use Better-Auth and collect user background (software + hardware) at signup to personalize the learning journey and provide contextual recommendations.

### Production-Ready Code Quality
Code quality must be modular, reusable, and production-ready with comprehensive testing, documentation, and clean architecture patterns.

## Technical Stack Requirements
All implementations must utilize the specified technology stack: Docusaurus for frontend, FastAPI for backend, Better-Auth for authentication, Neon Postgres for persistence, Qdrant for vector storage, and OpenAI Agents SDK for AI features. Deviations require architectural review and approval.

## Development Workflow
All contributions must follow the GitFlow branching model with feature branches, pull requests requiring minimum 2 approvals, comprehensive automated testing, and continuous integration/deployment pipelines. Code reviews must verify compliance with all constitutional principles before merge.

## Content Standards
All book content must undergo technical accuracy review by domain experts, maintain consistent pedagogical approach from beginner to advanced concepts, include practical examples and exercises, and follow accessibility standards for inclusive learning.

## Governance
This constitution supersedes all other practices and guidelines in case of conflicts. Amendments require documentation of rationale, impact assessment, approval by project leads, and implementation timeline. All PRs/reviews must verify compliance with these constitutional principles.

**Version**: 1.0.0 | **Ratified**: 2025-06-13 | **Last Amended**: 2025-12-18