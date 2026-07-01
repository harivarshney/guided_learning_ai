"""
Problem Understanding Agent
Analyzes student's question to understand what they're stuck on
"""

import json
import logging
from typing import Any, Dict
from groq import Groq
from .base_agent import Agent
from ..config import settings


logger = logging.getLogger(__name__)


class ProblemUnderstandingAgent(Agent):
    """
    Analyzes student question and returns:
    - What concept they're asking about
    - Their learning level (beginner/intermediate/advanced)
    - Common misconceptions for this concept
    - What part they're specifically stuck on
    """
    
    def __init__(self):
        super().__init__("Problem Understanding")
        self.client = Groq(api_key=settings.groq_api_key)
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze student question
        
        Args:
            input_data: {
                "question": "How do I build a REST API?",
                "context": "optional previous attempts"
            }
            
        Returns:
            {
                "concept": "REST API",
                "subconcepts": ["routing", "HTTP methods", "status codes"],
                "difficulty_level": "beginner",
                "stuck_at": "URL structure",
                "misconceptions": [...]
            }
        """
        self.log_start()
        
        if not await self.validate_input(input_data):
            return {"error": "Invalid input"}
        
        question = input_data.get("question", "")
        if not question:
            return {"error": "No question provided"}
        
        try:
            prompt = f"""Analyze this student question and respond ONLY with valid JSON:

Student question: {question}

Provide JSON with these fields:
1. concept: The main concept
2. subconcepts: List of sub-topics
3. difficulty_level: "beginner" or "intermediate" or "advanced"
4. stuck_at: What specific part are they confused about?
5. misconceptions: Common mistakes with this concept
6. learning_style_hint: code/explanation/analogy?

Respond ONLY with JSON, no extra text."""

            response = self.client.chat.completions.create(
               model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            response_text = response.choices[0].message.content
            
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            result = json.loads(response_text)
            
            self.log_end("success")
            return {"success": True, "data": result}
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return {"success": False, "error": str(e)}