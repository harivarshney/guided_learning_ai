"""
Pydantic Models for API Request/Response Validation
"""

from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel


# Question Schemas
class QuestionCreate(BaseModel):
    """Schema for creating a question"""
    user_id: str
    question: str
    concept: str
    difficulty_level: str
    context: Optional[str] = None


class QuestionResponse(BaseModel):
    """Schema for returning a question"""
    id: int
    user_id: str
    question: str
    concept: str
    difficulty_level: str
    context: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Response Schemas
class ResponseCreate(BaseModel):
    """Schema for creating a response"""
    question_id: int
    user_id: str
    problem_analysis: Optional[Any] = None
    resources: Optional[Any] = None
    explanation: Optional[Any] = None
    guidance: Optional[Any] = None
    practice: Optional[Any] = None


class ResponseReturn(BaseModel):
    """Schema for returning a response"""
    id: int
    question_id: int
    user_id: str
    problem_analysis: Optional[Any] = None
    resources: Optional[Any] = None
    explanation: Optional[Any] = None
    guidance: Optional[Any] = None
    practice: Optional[Any] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Progress Schemas
class ProgressCreate(BaseModel):
    """Schema for creating progress"""
    user_id: str
    question_id: int
    concept: str


class ProgressUpdate(BaseModel):
    """Schema for updating progress"""
    understanding_level: Optional[float] = None
    practice_completed: Optional[int] = None
    notes: Optional[str] = None


class ProgressResponse(BaseModel):
    """Schema for returning progress"""
    id: int
    user_id: str
    question_id: int
    concept: str
    times_asked: int
    last_asked: datetime
    understanding_level: float
    practice_completed: int
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Combined Response Schema
class FullLearningResponse(BaseModel):
    """Complete response with all agent outputs"""
    success: bool
    question: str
    user_id: str
    agents: dict
    summary: dict