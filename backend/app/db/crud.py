"""
CRUD Operations
Create, Read, Update, Delete database records
"""

import json
from sqlalchemy.orm import Session
from . import models
from datetime import datetime
from typing import Any, Dict, List


class QuestionCRUD:
    """Operations for StudentQuestion"""
    
    @staticmethod
    def create_question(db: Session, user_id: str, question: str, concept: str, difficulty_level: str, context: str = None):
        """Save a student question"""
        db_question = models.StudentQuestion(
            user_id=user_id,
            question=question,
            concept=concept,
            difficulty_level=difficulty_level,
            context=context
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return db_question
    
    @staticmethod
    def get_question(db: Session, question_id: int):
        """Get a question by ID"""
        return db.query(models.StudentQuestion).filter(
            models.StudentQuestion.id == question_id
        ).first()
    
    @staticmethod
    def get_user_questions(db: Session, user_id: str, limit: int = 10):
        """Get all questions for a user"""
        return db.query(models.StudentQuestion).filter(
            models.StudentQuestion.user_id == user_id
        ).order_by(models.StudentQuestion.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_concept_questions(db: Session, concept: str, limit: int = 10):
        """Get all questions for a concept"""
        return db.query(models.StudentQuestion).filter(
            models.StudentQuestion.concept == concept
        ).order_by(models.StudentQuestion.created_at.desc()).limit(limit).all()


class ResponseCRUD:
    """Operations for StudentResponse"""
    
    @staticmethod
    def create_response(
        db: Session,
        question_id: int,
        user_id: str,
        problem_analysis: Any,
        resources: Any,
        explanation: Any,
        guidance: Any,
        practice: Any,
        full_response_data: Dict[str, Any] = None
    ):
        """
        Save AI response to a question
        
        Args:
            question_id: ID of the question
            user_id: User who asked the question
            problem_analysis: Problem analysis data
            resources: Resources data
            explanation: Explanation data
            guidance: Guidance data
            practice: Practice problems data
            full_response_data: Full response object (unused for now)
        """
        # Convert to JSON if not already string
        def serialize(data):
            if isinstance(data, str):
                return data
            return json.dumps(data) if data else None
        
        db_response = models.StudentResponse(
            question_id=question_id,
            user_id=user_id,
            problem_analysis=serialize(problem_analysis),
            resources=serialize(resources),
            explanation=serialize(explanation),
            guidance=serialize(guidance),
            practice=serialize(practice)
        )
        db.add(db_response)
        db.commit()
        db.refresh(db_response)
        return db_response
    
    @staticmethod
    def get_response(db: Session, response_id: int):
        """Get a response by ID"""
        return db.query(models.StudentResponse).filter(
            models.StudentResponse.id == response_id
        ).first()
    
    @staticmethod
    def get_question_responses(db: Session, question_id: int):
        """Get all responses for a question"""
        return db.query(models.StudentResponse).filter(
            models.StudentResponse.question_id == question_id
        ).order_by(models.StudentResponse.created_at.desc()).all()
    
    @staticmethod
    def get_user_responses(db: Session, user_id: str, limit: int = 10):
        """Get all responses for a user"""
        return db.query(models.StudentResponse).filter(
            models.StudentResponse.user_id == user_id
        ).order_by(models.StudentResponse.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_response_data(db: Session, response_id: int) -> Dict[str, Any]:
        """
        Get response data in frontend-friendly format
        Returns the full response object for displaying in modal
        Reconstructs from individual fields
        """
        response = db.query(models.StudentResponse).filter(
            models.StudentResponse.id == response_id
        ).first()
        
        if not response:
            return None
        
        try:
            return {
                "agents": {
                    "problem_analysis": {"data": json.loads(response.problem_analysis) if response.problem_analysis else {}},
                    "resources": {"data": json.loads(response.resources) if response.resources else {}},
                    "explanation": {"data": json.loads(response.explanation) if response.explanation else {}},
                    "guidance": {"data": json.loads(response.guidance) if response.guidance else {}},
                    "practice": {"data": json.loads(response.practice) if response.practice else {}}
                }
            }
        except Exception as e:
            return None


class ProgressCRUD:
    """Operations for StudentProgress"""
    
    @staticmethod
    def create_progress(db: Session, user_id: str, question_id: int, concept: str):
        """Create new progress record"""
        db_progress = models.StudentProgress(
            user_id=user_id,
            question_id=question_id,
            concept=concept
        )
        db.add(db_progress)
        db.commit()
        db.refresh(db_progress)
        return db_progress
    
    @staticmethod
    def get_user_progress(db: Session, user_id: str):
        """Get all progress for a user"""
        return db.query(models.StudentProgress).filter(
            models.StudentProgress.user_id == user_id
        ).all()
    
    @staticmethod
    def get_concept_progress(db: Session, user_id: str, concept: str):
        """Get progress for a specific concept"""
        return db.query(models.StudentProgress).filter(
            models.StudentProgress.user_id == user_id,
            models.StudentProgress.concept == concept
        ).first()
    
    @staticmethod
    def update_progress(
        db: Session,
        progress_id: int,
        understanding_level: float = None,
        practice_completed: int = None,
        notes: str = None
    ):
        """Update progress record"""
        db_progress = db.query(models.StudentProgress).filter(
            models.StudentProgress.id == progress_id
        ).first()
        
        if db_progress:
            if understanding_level is not None:
                db_progress.understanding_level = understanding_level
            if practice_completed is not None:
                db_progress.practice_completed = practice_completed
            if notes is not None:
                db_progress.notes = notes
            db_progress.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_progress)
        
        return db_progress
    
    @staticmethod
    def increment_times_asked(db: Session, progress_id: int):
        """Increment times a concept was asked"""
        db_progress = db.query(models.StudentProgress).filter(
            models.StudentProgress.id == progress_id
        ).first()
        
        if db_progress:
            db_progress.times_asked += 1
            db_progress.last_asked = datetime.utcnow()
            db.commit()
            db.refresh(db_progress)
        
        return db_progress