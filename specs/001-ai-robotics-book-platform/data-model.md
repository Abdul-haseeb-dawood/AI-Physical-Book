# Data Model for AI & Robotics Book Platform

## User Profile
**Description**: Represents registered user information including skill level, software background, hardware/robotics experience, preferences, and learning history

**Fields**:
- `id` (string/UUID): Unique identifier for the user
- `email` (string): User's email address for authentication
- `skill_level` (enum): User's skill level (beginner, intermediate, advanced, expert)
- `software_background` (string): User's software development experience
- `hardware_experience` (string): User's hardware/robotics experience
- `preferences` (object): User preferences for UI, notifications, etc.
- `learning_history` (array): History of chapters read, quizzes taken, etc.
- `created_at` (datetime): Timestamp of account creation
- `updated_at` (datetime): Timestamp of last update

**Relationships**:
- One-to-many with ChatSession (user can have multiple chat sessions)
- One-to-many with PersonalizationProfile (user can have multiple personalization profiles)

**Validation Rules**:
- Email must be valid email format
- Skill level must be one of the defined enum values
- Learning history items must reference valid chapter IDs

## Book Chapter
**Description**: Represents individual book sections with content in multiple formats (English, Urdu), metadata, and connection to other chapters

**Fields**:
- `id` (string/UUID): Unique identifier for the chapter
- `title` (string): Title of the chapter
- `slug` (string): URL-friendly identifier for the chapter
- `content_en` (text): English content of the chapter in Markdown format
- `content_ur` (text): Urdu content of the chapter in Markdown format
- `metadata` (object): Additional chapter metadata (word count, estimated reading time, etc.)
- `previous_chapter_id` (string/UUID): ID of the previous chapter in the sequence
- `next_chapter_id` (string/UUID): ID of the next chapter in the sequence
- `section` (string): Section this chapter belongs to (e.g., "Foundations", "Advanced Topics")
- `difficulty_level` (enum): Difficulty level of the chapter (beginner, intermediate, advanced)
- `created_at` (datetime): Timestamp of chapter creation
- `updated_at` (datetime): Timestamp of last update

**Relationships**:
- One-to-many with TranslationPair (chapter can have multiple translations)
- Many-to-one with PersonalizationProfile (chapter can be personalized based on user profiles)

**Validation Rules**:
- Title and slug are required
- Content must be valid Markdown format
- Previous and next chapter IDs must reference valid existing chapters

## Chat Session
**Description**: Represents an interaction between a user and the RAG system, including query history and context

**Fields**:
- `id` (string/UUID): Unique identifier for the chat session
- `user_id` (string/UUID): ID of the user who initiated the session
- `chapter_id` (string/UUID): ID of the chapter context for the session (optional)
- `selected_text` (string): Text selected by the user for focused Q&A (optional)
- `query_history` (array): History of queries and responses in the session
- `mode` (enum): Chat mode (general, chapter-specific, selected-text-only)
- `created_at` (datetime): Timestamp of session creation
- `updated_at` (datetime): Timestamp of last interaction

**Relationships**:
- Many-to-one with UserProfile (multiple sessions per user)
- Many-to-one with BookChapter (session related to specific chapter)

**Validation Rules**:
- User ID is required
- Mode must be one of the defined enum values
- Query history items must have valid query and response fields

## Translation Pair
**Description**: Represents the relationship between English and Urdu versions of the same content

**Fields**:
- `id` (string/UUID): Unique identifier for the translation pair
- `chapter_id` (string/UUID): ID of the chapter this translation belongs to
- `content_en_id` (string/UUID): ID of the English content source
- `content_ur` (text): Urdu translation of the content
- `translation_quality` (enum): Quality rating of the translation (draft, reviewed, published)
- `translator_id` (string/UUID): ID of the translator (AI or human)
- `created_at` (datetime): Timestamp of translation creation
- `updated_at` (datetime): Timestamp of translation update

**Relationships**:
- Many-to-one with BookChapter (multiple translations per chapter)
- Many-to-one with UserProfile (if translated by a human)

**Validation Rules**:
- Chapter ID and content_en_id are required
- Translation quality must be one of the defined enum values

## Personalization Profile
**Description**: Represents personalized elements like summaries, recommendations, and adaptive content based on user background

**Fields**:
- `id` (string/UUID): Unique identifier for the personalization profile
- `user_id` (string/UUID): ID of the user this profile belongs to
- `chapter_id` (string/UUID): ID of the chapter this personalization applies to
- `personalized_summary` (text): Personalized summary based on user profile
- `recommended_prerequisites` (array): List of prerequisite topics or chapters based on user background
- `complexity_adjustment` (number): Adjustment factor for content complexity (0.5-2.0)
- `content_modifications` (object): Specific modifications to content based on user needs
- `created_at` (datetime): Timestamp of profile creation
- `updated_at` (datetime): Timestamp of last update

**Relationships**:
- Many-to-one with UserProfile (multiple profiles per user)
- Many-to-one with BookChapter (multiple personalizations per chapter)

**Validation Rules**:
- User ID and chapter ID are required
- Complexity adjustment must be between 0.5 and 2.0
- Recommended prerequisites must reference valid chapter IDs