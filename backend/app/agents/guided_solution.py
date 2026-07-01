import logging
import json
from typing import Any, Dict, List
from groq import Groq
from .base_agent import Agent
from ..config import settings


logger = logging.getLogger(__name__)


class GuidedSolutionAgent(Agent):
    """
    Guides students through solving problems step-by-step.
    Never gives direct answers - teaches problem-solving approach.
    Returns structured steps for beautiful UI rendering.
    """
    
    def __init__(self):
        super().__init__("Guided Solution")
        self.client = Groq(api_key=settings.groq_api_key)
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide guided steps to solve a problem
        """
        self.log_start()
        
        if not await self.validate_input(input_data):
            return {"error": "Invalid input"}
        
        concept = input_data.get("concept", "")
        problem = input_data.get("problem", "")
        difficulty = input_data.get("difficulty_level", "beginner")
        
        if not concept or not problem:
            return {"error": "Concept and problem required"}
        
        try:
            # Create structured guidance steps
            prompt = f"""Break down this problem into clear steps.
Problem: {problem}
Concept: {concept}
Level: {difficulty}

Return ONLY a JSON array with exactly 5 steps. NO markdown, NO backticks, NO extra text:

[
  {{"step_number": 1, "title": "Understanding", "description": "...", "hint": "...", "thinking_question": "...?"}},
  {{"step_number": 2, "title": "Planning", "description": "...", "hint": "...", "thinking_question": "...?"}},
  {{"step_number": 3, "title": "Breaking Down", "description": "...", "hint": "...", "thinking_question": "...?"}},
  {{"step_number": 4, "title": "Implementing", "description": "...", "hint": "...", "thinking_question": "...?"}},
  {{"step_number": 5, "title": "Verifying", "description": "...", "hint": "...", "thinking_question": "...?"}}
]

Keep descriptions short (1-2 sentences). Keep hints subtle. Keep questions simple."""

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=1200
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean up response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse the steps array
            try:
                steps_array = json.loads(response_text)
                
                # Ensure it's a list
                if not isinstance(steps_array, list):
                    steps_array = [steps_array]
                
                # Build final guidance object
                guidance_object = {
                    "steps": steps_array,
                    "encouragement": f"Great! You're learning {concept}. Take it step by step and you'll solve this!"
                }
                
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON parse error: {e}")
                # Fallback: create default steps
                guidance_object = {
                    "steps": [
                        {"step_number": 1, "title": "Understanding", "description": "Read the problem carefully", "hint": "What are you asked to do?", "thinking_question": "What do you need to understand?"},
                        {"step_number": 2, "title": "Planning", "description": "Think about your approach", "hint": "How will you tackle this?", "thinking_question": "What's your strategy?"},
                        {"step_number": 3, "title": "Breaking Down", "description": "Divide into smaller parts", "hint": "What are the main parts?", "thinking_question": "How can you break this down?"},
                        {"step_number": 4, "title": "Implementing", "description": "Work through step by step", "hint": "Take it one piece at a time", "thinking_question": "How will you build this?"},
                        {"step_number": 5, "title": "Verifying", "description": "Check your solution", "hint": "Does it work?", "thinking_question": "How do you know it's correct?"}
                    ],
                    "encouragement": f"Keep going! You're making progress with {concept}!"
                }
            
            self.log_end("success")
            return {
                "success": True,
                "data": {
                    "concept": concept,
                    "guidance": guidance_object
                }
            }
        
        except Exception as e:
            self.logger.error(f"Error in guidance: {e}")
            # Return safe fallback
            return {
                "success": True,
                "data": {
                    "concept": concept,
                    "guidance": {
                        "steps": [
                            {"step_number": 1, "title": "Start", "description": "Understand the problem", "hint": "Read carefully", "thinking_question": "What is being asked?"}
                        ],
                        "encouragement": "You've got this!"
                    }
                }
            }
