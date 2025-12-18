# API Contract for AI & Robotics Book Platform

## User Authentication API

### POST /api/auth/register
**Description**: Register a new user with their background information

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "skill_level": "intermediate",
  "software_background": "5 years of Python and JavaScript experience",
  "hardware_experience": "Experience with Arduino and basic electronics"
}
```

**Response (201 Created)**:
```json
{
  "id": "user-uuid-123",
  "email": "user@example.com",
  "skill_level": "intermediate",
  "created_at": "2025-12-18T10:00:00Z"
}
```

### POST /api/auth/login
**Description**: Authenticate a user and return session token

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK)**:
```json
{
  "token": "jwt-token-string",
  "user": {
    "id": "user-uuid-123",
    "email": "user@example.com",
    "skill_level": "intermediate"
  }
}
```

## Book Content API

### GET /api/chapters
**Description**: Retrieve all book chapters

**Response (200 OK)**:
```json
{
  "chapters": [
    {
      "id": "chapter-uuid-001",
      "title": "Introduction to Physical AI",
      "slug": "introduction-to-physical-ai",
      "difficulty_level": "beginner",
      "section": "Foundations",
      "previous_chapter_id": null,
      "next_chapter_id": "chapter-uuid-002"
    }
  ]
}
```

### GET /api/chapters/{slug}
**Description**: Retrieve a specific chapter by slug with content

**Parameters**: 
- slug (path): URL-friendly identifier for the chapter

**Response (200 OK)**:
```json
{
  "id": "chapter-uuid-001",
  "title": "Introduction to Physical AI",
  "slug": "introduction-to-physical-ai",
  "difficulty_level": "beginner",
  "content_en": "# Introduction to Physical AI\n\nPhysical AI refers to the intersection of artificial intelligence and physical systems...",
  "content_ur": "# جسمانی مصنوعی ذہانت کا تعارف\n\nجسمانی مصنوعی ذہانت مصنوعی ذہانت اور جسمانی نظام کے تال میں شامل ہوتا ہے...",
  "previous_chapter_id": null,
  "next_chapter_id": "chapter-uuid-002"
}
```

## Chatbot API

### POST /api/chat/start-session
**Description**: Create a new chat session with the RAG system

**Headers**: 
- Authorization: Bearer {token}

**Request Body**:
```json
{
  "chapter_id": "chapter-uuid-001",
  "selected_text": "Physical AI refers to the intersection of artificial intelligence and physical systems...",
  "mode": "selected-text-only" // Options: general, chapter-specific, selected-text-only
}
```

**Response (201 Created)**:
```json
{
  "session_id": "session-uuid-456",
  "chapter_id": "chapter-uuid-001",
  "selected_text": "Physical AI refers to the intersection of artificial intelligence and physical systems...",
  "mode": "selected-text-only",
  "created_at": "2025-12-18T10:00:00Z"
}
```

### POST /api/chat/{session_id}/query
**Description**: Submit a query to the RAG system in a specific session

**Headers**: 
- Authorization: Bearer {token}

**Parameters**: 
- session_id (path): ID of the chat session

**Request Body**:
```json
{
  "query": "What are the key components of Physical AI?"
}
```

**Response (200 OK)**:
```json
{
  "query": "What are the key components of Physical AI?",
  "response": "The key components of Physical AI include: sensors for perception, actuators for action, control systems for coordination, and AI algorithms for decision making.",
  "sources": ["introduction-to-physical-ai", "foundations-of-robotics"],
  "timestamp": "2025-12-18T10:00:00Z"
}
```

## Personalization API

### GET /api/personalization/profile
**Description**: Retrieve user's personalization profile for a specific chapter

**Headers**: 
- Authorization: Bearer {token}

**Query Parameters**: 
- chapter_id (query): ID of the chapter to get personalization for

**Response (200 OK)**:
```json
{
  "profile": {
    "id": "profile-uuid-789",
    "user_id": "user-uuid-123",
    "chapter_id": "chapter-uuid-001",
    "personalized_summary": "As an intermediate Python developer with hardware experience, this chapter covers the fundamentals of how AI algorithms interact with physical systems...",
    "recommended_prerequisites": ["foundations-of-robotics", "sensors-perception"],
    "complexity_adjustment": 1.2
  }
}
```

### POST /api/personalization/profile
**Description**: Create or update user's personalization profile

**Headers**: 
- Authorization: Bearer {token}

**Request Body**:
```json
{
  "chapter_id": "chapter-uuid-001",
  "personalized_summary": "As an intermediate Python developer with hardware experience, this chapter covers the fundamentals of how AI algorithms interact with physical systems...",
  "recommended_prerequisites": ["foundations-of-robotics", "sensors-perception"],
  "complexity_adjustment": 1.2
}
```

**Response (201 Created)**:
```json
{
  "profile": {
    "id": "profile-uuid-789",
    "user_id": "user-uuid-123",
    "chapter_id": "chapter-uuid-001",
    "personalized_summary": "As an intermediate Python developer with hardware experience, this chapter covers the fundamentals of how AI algorithms interact with physical systems...",
    "recommended_prerequisites": ["foundations-of-robotics", "sensors-perception"],
    "complexity_adjustment": 1.2,
    "updated_at": "2025-12-18T10:00:00Z"
  }
}
```

## Translation API

### PUT /api/translation/toggle
**Description**: Toggle the language preference for a chapter

**Headers**: 
- Authorization: Bearer {token}

**Request Body**:
```json
{
  "chapter_slug": "introduction-to-physical-ai",
  "target_language": "ur" // Options: en, ur
}
```

**Response (200 OK)**:
```json
{
  "chapter_slug": "introduction-to-physical-ai",
  "current_language": "ur",
  "available_languages": ["en", "ur"]
}
```