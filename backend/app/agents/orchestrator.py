"""
Agent Orchestrator - Coordinates all agents
Week 1: Problem Understanding Agent
Week 2: + Resource Finder Agent
Week 3: + Concept Explainer, Guided Solution, Practice Generator
"""

import asyncio
import logging
from typing import Any, Dict

from .problem_understanding import ProblemUnderstandingAgent
from .resource_finder import ResourceFinderAgent
from .concept_explainer import ConceptExplainerAgent
from .guided_solution import GuidedSolutionAgent
from .practice_generator import PracticeGeneratorAgent


logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Orchestrates all agents to provide comprehensive learning guidance
    """
    
    def __init__(self):
        """Initialize all agents"""
        self.problem_agent = ProblemUnderstandingAgent()
        self.resource_agent = ResourceFinderAgent()
        self.explainer_agent = ConceptExplainerAgent()
        self.solution_agent = GuidedSolutionAgent()
        self.practice_agent = PracticeGeneratorAgent()
        logger.info("✅ Orchestrator initialized with 5 agents")
    
    async def orchestrate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run all agents in optimized sequence:
        1. Problem Understanding (required first)
        2. Run remaining 4 agents in parallel
        
        Args:
            input_data: {
                "question": "...",
                "user_id": "...",
                "context": "..."
            }
            
        Returns:
            Complete learning guidance with all agent outputs
        """
        logger.info(f"🎯 Orchestrator started for question: {input_data.get('question')}")
        
        try:
            question = input_data.get("question", "")
            user_id = input_data.get("user_id", "anonymous")
            
            # STEP 1: Analyze problem first (needed for other agents)
            logger.info("Step 1: Analyzing problem...")
            problem_result = await self.problem_agent.run({
                "question": question,
                "context": input_data.get("context", "")
            })
            
            # Extract concept and difficulty for other agents
            concept = "General"
            difficulty = "beginner"
            
            if problem_result.get("success"):
                concept = problem_result.get("data", {}).get("concept", "General")
                difficulty = problem_result.get("data", {}).get("difficulty_level", "beginner")
            
            logger.info(f"Problem analyzed: {concept} ({difficulty})")
            
            # STEP 2: Run all other agents in parallel
            logger.info("Step 2: Running all agents in parallel...")
            
            resource_task = asyncio.create_task(
                self.resource_agent.run({
                    "concept": concept,
                    "difficulty_level": difficulty
                })
            )
            
            explainer_task = asyncio.create_task(
                self.explainer_agent.run({
                    "concept": concept,
                    "difficulty_level": difficulty,
                    "context": input_data.get("context", "")
                })
            )
            
            solution_task = asyncio.create_task(
                self.solution_agent.run({
                    "concept": concept,
                    "problem": question,
                    "difficulty_level": difficulty,
                    "student_attempt": input_data.get("student_attempt", "")
                })
            )
            
            practice_task = asyncio.create_task(
                self.practice_agent.run({
                    "concept": concept,
                    "difficulty_level": difficulty,
                    "num_problems": 3
                })
            )
            
            # Wait for all parallel tasks
            resource_result, explainer_result, solution_result, practice_result = await asyncio.gather(
                resource_task,
                explainer_task,
                solution_task,
                practice_task
            )
            
            logger.info("All agents completed successfully")
            
            # STEP 3: Combine all results
            response = {
                "success": True,
                "question": question,
                "user_id": user_id,
                "agents": {
                    "problem_analysis": problem_result,
                    "resources": resource_result,
                    "explanation": explainer_result,
                    "guidance": solution_result,
                    "practice": practice_result
                },
                "summary": {
                    "concept": concept,
                    "difficulty_level": difficulty,
                    "total_resources": len(resource_result.get("data", {}).get("resources", [])) if resource_result.get("success") else 0,
                    "practice_problems": len(practice_result.get("data", {}).get("problems", [])) if practice_result.get("success") else 0
                }
            }
            
            logger.info("✅ Orchestration complete - full learning guidance generated")
            return response
        
        except asyncio.TimeoutError:
            logger.error("❌ Orchestration timeout - agents took too long")
            return {
                "success": False,
                "error": "Processing timeout - please try again"
            }
        
        except Exception as e:
            logger.error(f"❌ Orchestration error: {e}")
            return {
                "success": False,
                "error": str(e)
            }