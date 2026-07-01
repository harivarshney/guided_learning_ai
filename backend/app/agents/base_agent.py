"""
Base Agent class - Parent for all agents
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging


logger = logging.getLogger(__name__)


class Agent(ABC):
    """
    Base class for all agents.
    Each agent specializes in a specific task.
    """
    
    def __init__(self, name: str):
        """
        Initialize agent
        
        Args:
            name: Agent name (e.g., "Problem Understanding")
        """
        self.name = name
        self.logger = logging.getLogger(f"agents.{name}")
    
    @abstractmethod
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the agent with input data
        
        Args:
            input_data: Dictionary with agent-specific input
            
        Returns:
            Dictionary with agent results
        """
        pass
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate input before processing
        
        Args:
            input_data: Input to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(input_data, dict):
            self.logger.error(f"{self.name}: Input must be a dictionary")
            return False
        return True
    
    def log_start(self):
        """Log when agent starts processing"""
        self.logger.info(f"{self.name} agent started")
    
    def log_end(self, status: str = "success"):
        """Log when agent finishes"""
        self.logger.info(f"{self.name} agent finished ({status})")