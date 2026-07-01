"""
SQLAlchemy Database Models
Tables: Questions, Responses, StudentProgress
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class StudentQuestion(Base):
    """Store student questions"""
    __tablename__ = "student_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    question = Column(Text)
    context = Column(Text, nullable=True)
    concept = Column(String(255), index=True)
    difficulty_level = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    responses = relationship("StudentResponse", back_populates="question")
    progress = relationship("StudentProgress", back_populates="question")


class StudentResponse(Base):
    """Store AI responses to questions"""
    __tablename__ = "student_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("student_questions.id"), index=True)
    user_id = Column(String(255), index=True)
    
    # Response from each agent
    problem_analysis = Column(JSON)
    resources = Column(JSON)
    explanation = Column(JSON)
    guidance = Column(JSON)
    practice = Column(JSON)
    
    # Full response data for history modal reconstruction
    
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    question = relationship("StudentQuestion", back_populates="responses")


class StudentProgress(Base):
    """Track student progress"""
    __tablename__ = "student_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    question_id = Column(Integer, ForeignKey("student_questions.id"), index=True)
    concept = Column(String(255), index=True)
    
    # Progress tracking
    times_asked = Column(Integer, default=1)
    last_asked = Column(DateTime, default=datetime.utcnow)
    understanding_level = Column(Float, default=0.0)  # 0-100
    practice_completed = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    question = relationship("StudentQuestion", back_populates="progress")