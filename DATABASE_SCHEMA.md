# Database Schema - Guided Learning AI

This document outlines the PostgreSQL database structure used in the Guided Learning AI application.

## Database Connection
- **Provider**: Railway PostgreSQL
- **ORM**: SQLAlchemy
- **Models Location**: `backend/app/db/models.py`

---

## Tables

### 1. Users Table
Stores user information and tracks unique learners.

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Fields:**
- `id`: Auto-incrementing primary key
- `user_id`: Unique identifier for each user (persisted in browser localStorage)
- `name`: User's display name
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

**Indexes:**
- Primary key on `id`
- Unique index on `user_id`

---

### 2. Questions Table
Stores every question asked by users and all associated AI-generated responses.

```sql
CREATE TABLE questions (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  question TEXT NOT NULL,
  concept VARCHAR(255),
  difficulty VARCHAR(50),
  
  problem_analysis TEXT,
  resources TEXT,
  explanation TEXT,
  guidance TEXT,
  questions_data TEXT,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

**Fields:**
- `id`: Auto-incrementing primary key
- `user_id`: Foreign key linking to users table
- `question`: The original question asked by student
- `concept`: Main concept/topic being asked about
- `difficulty`: Difficulty level (Beginner, Intermediate, Advanced)
- `problem_analysis`: JSON from Problem Understanding Agent
- `resources`: JSON from Resource Finder Agent (Wikipedia, YouTube, GitHub links)
- `explanation`: JSON from Concept Explainer Agent (deep explanation with 15+ sections)
- `guidance`: JSON from Guided Solution Agent (5 step-by-step guidance)
- `questions_data`: JSON from Question Generator Agent (20 study questions with answers)
- `created_at`: When question was asked
- `updated_at`: Last update timestamp

**Data Format (JSON):**
All agent responses stored as JSON strings:
```json
{
  "problem_analysis": {
    "understanding": "...",
    "key_issues": [...]
  },
  "resources": {
    "wikipedia": "...",
    "youtube": "...",
    "github": "...",
    "devto": "..."
  },
  "explanation": {
    "overview": "...",
    "history": {...},
    "core_principles": [...],
    "step_by_step_breakdown": [...],
    "real_world_applications": [...],
    "key_concepts": [...],
    "analogies": [...],
    "comparisons": {...},
    "advantages": [...],
    "limitations": [...],
    "best_practices": [...],
    "common_mistakes": [...],
    "why_it_matters": "..."
  },
  "guidance": {
    "steps": [
      {
        "step_number": 1,
        "title": "...",
        "hint": "...",
        "thinking_question": "..."
      }
    ],
    "encouragement": "..."
  },
  "questions_data": {
    "problems": [
      {
        "question_number": 1,
        "importance": "⭐",
        "question": "...",
        "answer": "...",
        "explanation": "...",
        "difficulty": "Beginner"
      }
    ],
    "total_problems": 20
  }
}
```

**Indexes:**
- Primary key on `id`
- Foreign key on `user_id`
- Index on `created_at` (for sorting history by date)
- Index on `user_id` (for fetching user's questions)

---

### 3. Progress Table
Tracks learning progress per concept for each user.

```sql
CREATE TABLE progress (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  concept VARCHAR(255) NOT NULL,
  
  understanding_level FLOAT DEFAULT 0,
  times_asked INTEGER DEFAULT 1,
  practice_completed INTEGER DEFAULT 0,
  
  last_asked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  notes TEXT,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  UNIQUE KEY unique_user_concept (user_id, concept)
);
```

**Fields:**
- `id`: Auto-incrementing primary key
- `user_id`: Foreign key linking to users table
- `concept`: The concept/topic being tracked
- `understanding_level`: Float (0-100) representing mastery percentage
- `times_asked`: How many times user asked about this concept
- `practice_completed`: Number of practice problems completed
- `last_asked`: When concept was last asked about
- `notes`: Optional notes about progress
- `created_at`: When progress tracking started
- `updated_at`: Last update timestamp

**Constraints:**
- Composite unique constraint on `(user_id, concept)` - one record per user per concept

**Indexes:**
- Primary key on `id`
- Foreign key on `user_id`
- Unique index on `(user_id, concept)`

---

## Data Flow

```
User Asks Question
        ↓
5 AI Agents Process
        ↓
Results stored in Questions table
        ↓
Progress table updated/created
        ↓
User can view:
  - Full response in tabbed interface
  - History of all questions
  - Progress dashboard
```

---

## Query Examples

### Get user's learning history
```sql
SELECT id, question, concept, difficulty, created_at 
FROM questions 
WHERE user_id = 'user_id_here' 
ORDER BY created_at DESC;
```

### Get user's progress on all concepts
```sql
SELECT concept, understanding_level, times_asked, practice_completed, last_asked 
FROM progress 
WHERE user_id = 'user_id_here' 
ORDER BY understanding_level DESC;
```

### Get average understanding across all concepts
```sql
SELECT AVG(understanding_level) as avg_understanding, COUNT(DISTINCT concept) as concepts_learned
FROM progress 
WHERE user_id = 'user_id_here';
```

### Get most frequently asked concepts
```sql
SELECT concept, times_asked, understanding_level 
FROM progress 
WHERE user_id = 'user_id_here' 
ORDER BY times_asked DESC 
LIMIT 10;
```

---

## Database Initialization

When deploying to Railway:
1. PostgreSQL database is automatically created
2. SQLAlchemy models auto-create tables on first run
3. Connection string stored in `.env` as `DATABASE_URL`

**No manual SQL setup needed!** The ORM handles table creation.

---

## Data Retention & Privacy

- ✅ All user data is stored in PostgreSQL on Railway
- ✅ Responses are JSON-stored for flexibility
- ✅ No API keys or secrets stored in database
- ✅ User can request data deletion (GDPR-compliant design)
- ✅ Data persists across sessions via user_id

---

## Performance Considerations

- **Indexes**: Created on frequently queried fields (user_id, created_at)
- **JSON Storage**: Allows flexibility without complex schemas
- **Unique Constraints**: Prevent duplicate progress records
- **Query Optimization**: Use indexes for fast retrieval

---

## Future Enhancements

- Add tags to questions for better categorization
- Track question-to-answer feedback loops
- Add spaced repetition scheduling
- Implement learning paths/courses
- Add collaborative learning features
