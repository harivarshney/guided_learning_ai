import logging
import json
from typing import Any, Dict
from groq import Groq
from .base_agent import Agent
from ..config import settings


logger = logging.getLogger(__name__)


class ConceptExplainerAgent(Agent):
    """
    Provides DEEP, comprehensive explanations of concepts.
    
    Includes:
    - Historical context & origins
    - Creator/developer information
    - Why it was created & its necessity
    - Core principles & theory
    - Real-world applications
    - Step-by-step breakdown
    - Comparisons with similar concepts
    - Best practices & common mistakes
    """
    
    def __init__(self):
        super().__init__("Concept Explainer")
        self.client = Groq(api_key=settings.groq_api_key)
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide deep explanation of a concept
        
        Args:
            input_data: {
                "concept": "Python",
                "difficulty_level": "beginner",
                "context": "optional"
            }
            
        Returns:
            {
                "concept": "Python",
                "explanation": {
                    "overview": "...",
                    "history": {
                        "created_when": "...",
                        "created_by": "...",
                        "why_created": "..."
                    },
                    "core_principles": ["...", "..."],
                    "step_by_step": ["...", "..."],
                    "real_world_applications": ["...", "..."],
                    "comparisons": {"vs_X": "...", "vs_Y": "..."},
                    "key_concepts": ["...", "..."],
                    "best_practices": ["...", "..."],
                    "common_mistakes": ["...", "..."],
                    "why_it_matters": "..."
                }
            }
        """
        self.log_start()
        
        if not await self.validate_input(input_data):
            return {"error": "Invalid input"}
        
        concept = input_data.get("concept", "").strip()
        difficulty = input_data.get("difficulty_level", "beginner")
        
        if not concept:
            return {"error": "No concept provided"}
        
        try:
            prompt = f"""You are an expert educator. Provide a COMPREHENSIVE, DEEP explanation of '{concept}' for a {difficulty} learner.

Return ONLY valid JSON (no markdown, no backticks):

{{
  "overview": "1-2 sentence simple definition",
  "history": {{
    "created_when": "When was it created/discovered? (year/period)",
    "created_by": "Who created/developed it? (names/organizations)",
    "why_created": "Why was it needed? What problem did it solve? (2-3 sentences)",
    "evolution": "How has it evolved since then? (2-3 sentences)"
  }},
  "core_principles": [
    "First core principle/concept",
    "Second core principle/concept",
    "Third core principle/concept",
    "Fourth principle if applicable"
  ],
  "step_by_step_breakdown": [
    "1. First concept explained",
    "2. Second concept explained",
    "3. Third concept explained",
    "4. Fourth concept explained",
    "5. How they connect together"
  ],
  "real_world_applications": [
    "Application 1: Specific example with context",
    "Application 2: Specific example with context",
    "Application 3: Specific example with context",
    "Application 4: Specific example with context"
  ],
  "key_concepts": [
    "Key term 1: Brief explanation",
    "Key term 2: Brief explanation",
    "Key term 3: Brief explanation",
    "Key term 4: Brief explanation"
  ],
  "analogies": [
    "Real-world analogy 1: Simple comparison",
    "Real-world analogy 2: Simple comparison"
  ],
  "comparisons": {{
    "vs_similar_concept_1": "How different from [similar concept]?",
    "vs_similar_concept_2": "How different from [similar concept]?"
  }},
  "advantages": [
    "Major advantage 1",
    "Major advantage 2",
    "Major advantage 3"
  ],
  "limitations": [
    "Important limitation 1",
    "Important limitation 2",
    "Important limitation 3"
  ],
  "best_practices": [
    "Best practice 1 with explanation",
    "Best practice 2 with explanation",
    "Best practice 3 with explanation"
  ],
  "common_mistakes": [
    "Common mistake 1: What beginners do wrong and why",
    "Common mistake 2: What beginners do wrong and why",
    "Common mistake 3: What beginners do wrong and why"
  ],
  "why_it_matters": "Why should someone care about this concept? How does it impact their learning/career? (2-3 sentences)"
}}

Be thorough, educational, and make it suitable for someone learning this for the first time!"""

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean markdown if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            response_text = response_text.strip()
            
            try:
                explanation = json.loads(response_text)
            except json.JSONDecodeError as e:
                logger.error(f"JSON parse error: {e}")
                explanation = {
                    "overview": response_text,
                    "error": "Could not parse structured response"
                }
            
            self.log_end("success")
            return {
                "success": True,
                "data": {
                    "concept": concept,
                    "difficulty_level": difficulty,
                    "explanation": explanation
                }
            }
        
        except Exception as e:
            self.logger.error(f"Error explaining concept: {e}")
            return {
                "success": False,
                "error": str(e)
            }
