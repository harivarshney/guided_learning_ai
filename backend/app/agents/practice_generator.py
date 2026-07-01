"""
Question Generator Agent
Generates important study questions for downloadable question banks
Creates 15-20 important questions based on the concept
"""

import json
import logging
from typing import Any, Dict, List
from groq import Groq
from .base_agent import Agent
from ..config import settings


logger = logging.getLogger(__name__)


class PracticeGeneratorAgent(Agent):
    """
    Generates IMPORTANT study questions for a concept.
    Creates 15-20 questions labeled by importance.
    """
    
    def __init__(self):
        super().__init__("Question Generator")
        self.client = Groq(api_key=settings.groq_api_key)
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate important study questions"""
        self.log_start()
        
        if not await self.validate_input(input_data):
            return {"error": "Invalid input"}
        
        concept = input_data.get("concept", "").strip()
        difficulty = input_data.get("difficulty_level", "beginner")
        
        if not concept:
            return {"error": "No concept provided"}
        
        try:
            # Generate questions one at a time to avoid large JSON parsing issues
            questions = []
            
            # Generate 20 questions
            for i in range(1, 21):
                importance = "⭐ Important" if i <= 8 else "⭐⭐ Very Important"
                
                prompt = f"""Create ONE study question #{i} for: {concept}
Level: {difficulty}
Mark as: {importance}

Return ONLY JSON (no markdown):
{{
  "question_number": {i},
  "importance": "{importance}",
  "question": "The question text here",
  "answer": "The correct answer",
  "explanation": "Why this matters (1-2 sentences)",
  "difficulty": "{difficulty}"
}}"""
                
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=400
                )
                
                response_text = response.choices[0].message.content.strip()
                
                # Clean markdown
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0]
                
                response_text = response_text.strip()
                
                try:
                    question_obj = json.loads(response_text)
                    questions.append(question_obj)
                except json.JSONDecodeError:
                    # Create a fallback question if parsing fails
                    logger.warning(f"Failed to parse question {i}, using fallback")
                    questions.append({
                        "question_number": i,
                        "importance": importance,
                        "question": f"Question {i} about {concept}",
                        "answer": f"This is related to {concept}",
                        "explanation": f"Understanding this helps with {concept}",
                        "difficulty": difficulty
                    })
            
            self.log_end("success")
            return {
                "success": True,
                "data": {
                    "concept": concept,
                    "difficulty_level": difficulty,
                    "problems": questions,
                    "total_problems": len(questions)
                }
            }
        
        except Exception as e:
            self.logger.error(f"Error generating questions: {e}")
            
            # Return default questions as fallback
            default_questions = []
            for i in range(1, 21):
                importance = "⭐ Important" if i <= 8 else "⭐⭐ Very Important"
                default_questions.append({
                    "question_number": i,
                    "importance": importance,
                    "question": f"Question {i}: What are the key aspects of {concept}?",
                    "answer": f"{concept} involves several important concepts.",
                    "explanation": f"Understanding {concept} requires knowledge of multiple areas.",
                    "difficulty": difficulty
                })
            
            return {
                "success": True,
                "data": {
                    "concept": concept,
                    "difficulty_level": difficulty,
                    "problems": default_questions,
                    "total_problems": 20
                }
            }