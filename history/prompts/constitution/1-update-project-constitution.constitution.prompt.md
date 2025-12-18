---
id: 1
title: Update Project Constitution
stage: constitution
date: 2025-12-18
surface: agent
model: Qwen
feature: none
branch: main
user: hp
command: /sp.constitution
labels: ["constitution","setup","governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution You are an expert AI Book Architect, RAG Systems Engineer, and UI/UX Designer.

This project follows these non-negotiable constitutional principles:

1. The book title is **"Physical AI & Humanoid Robotics"**
2. The book must be written using **Docusaurus** and deployed on **GitHub Pages**
3. Content must be:

   * Technically accurate
   * Beginner to advanced friendly
   * Structured like a real academic + industry book
4. All chapters must support:

   * Personalization for logged-in users
   * Urdu translation toggle
5. UI must be:

   * Premium / VIP quality
   * Interactive, modern, dark-mode friendly
   * Smooth animations and readable typography
6. A **RAG chatbot** must be embedded inside the book:

   * Answers ONLY from book content
   * Can answer based on user-selected text
7. Backend stack is fixed:

   * FastAPI
   * OpenAI Agents / ChatKit SDK
   * Neon Serverless Postgres
   * Qdrant Cloud (Free Tier)
8. Authentication must use **Better-Auth**
9. User background (software + hardware) must be collected at signup
10. Code quality must be modular, reusable, and production-ready

If any requirement conflicts, prioritize:
Accuracy > UX > Performance > Extra features

## Response snapshot

I've successfully created the project constitution for your "Physical AI & Humanoid Robotics" book. Based on your specifications, I've replaced all placeholders in the template with project-specific information and organized the principles into clear sections. The constitution now includes:

1. Core Principles based on your requirements:
   - Book Title & Platform
   - Content Quality Standards
   - Personalization & Localization Features
   - Premium UI/UX Experience
   - Integrated RAG Chatbot
   - Fixed Backend Technology Stack
   - User Authentication & Profiling
   - Production-Ready Code Quality

2. Additional sections:
   - Technical Stack Requirements
   - Development Workflow
   - Content Standards
   - Governance

The constitution file has been saved to `.specify/memory/constitution.md` with version 1.0.0, and includes an HTML comment at the top with a sync impact report. I've also created this Prompt History Record as required.

## Outcome

- ✅ Impact: Created project constitution with all specified principles
- 🧪 Tests: N/A (documentation update)
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: Development can proceed using these constitutional principles
- 🧠 Reflection: The constitution clearly defines the project scope and technology stack to guide future development decisions

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): Standard constitution update
- Next experiment (smallest change to try): N/A
