import logging
import os
from typing import Any, Dict, List
from groq import Groq
from dotenv import load_dotenv
from .base_agent import Agent
from urllib.parse import quote

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class ResourceFinderAgent(Agent):
    """
    Intelligent Educational Resource Discovery Agent v2.0
    
    Provides curated learning resources across ALL domains with:
    - Zero broken links (uses search URLs)
    - Wikipedia integration (covers everything)
    - GitHub examples and implementations
    - Dev.to community tutorials
    - YouTube video search
    - Official documentation
    
    Domain Coverage:
    - Mathematics (Class 2 → Advanced Calculus)
    - Science (Physics, Chemistry, Biology)
    - Computer Science (DSA, Algorithms, System Design)
    - Web Development (Frontend, Backend, Full-stack)
    - Data Science & Machine Learning
    - Cloud & DevOps
    - Languages & Literature
    - And basically ANY educational topic
    """
    
    def __init__(self):
        """Initialize Resource Finder with Groq LLM and search URL builder."""
        super().__init__("Resource Finder")
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not configured. Set it in your .env file."
            )
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute resource discovery for any learning topic.
        
        Args:
            input_data: {
                "concept": "Machine Learning fundamentals",
                "difficulty_level": "beginner"
            }
        
        Returns:
            {
                "success": bool,
                "data": {
                    "concept": str,
                    "extracted_concepts": List[str],
                    "resources": List[Dict],  # Wikipedia, GitHub, Dev.to, YouTube, Docs
                    "total_found": int
                }
            }
        """
        self.log_start()
        
        if not await self.validate_input(input_data):
            return {"error": "Invalid input"}
        
        concept: str = input_data.get("concept", "").strip()
        difficulty: str = input_data.get("difficulty_level", "beginner")
        
        if not concept:
            return {"error": "Concept parameter required"}
        
        try:
            # Extract core concepts using LLM
            extracted_concepts = self._extract_concepts_with_groq(concept, difficulty)
            
            resources: List[Dict[str, Any]] = []
            
            # Build search URLs for all resource types
            resources.extend(self._generate_wikipedia_resources(extracted_concepts))
            resources.extend(self._generate_youtube_resources(extracted_concepts))
            resources.extend(self._generate_github_resources(extracted_concepts))
            resources.extend(self._generate_devto_resources(extracted_concepts))
            resources.extend(self._generate_documentation_resources(extracted_concepts))
            
            self.log_end("success")
            
            return {
                "success": True,
                "data": {
                    "concept": concept,
                    "extracted_concepts": extracted_concepts,
                    "resources": resources,
                    "total_found": len(resources)
                }
            }
        
        except Exception as e:
            self.logger.error(f"Resource discovery failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "data": {"resources": []}
            }
    
    def _extract_concepts_with_groq(self, concept: str, difficulty: str) -> List[str]:
        """
        Use Groq LLM to intelligently extract core learning concepts.
        
        Handles any topic: Maths, Science, Programming, Languages, etc.
        
        Args:
            concept: User's learning query
            difficulty: Target difficulty level
        
        Returns:
            List of core concept names
        """
        try:
            prompt = f"""
            Analyze this learning query and extract 2-3 core concepts:
            
            Query: "{concept}"
            Level: {difficulty}
            
            Extract the main topics a student should learn.
            Be smart about handling:
            - Variations (e.g., "ML" = "Machine Learning")
            - Combinations (e.g., "web dev" = "JavaScript", "React", "Backend")
            - General queries (e.g., "science" = specific science domains)
            - Academic levels (e.g., "class 10 physics" = relevant physics topics)
            
            Return ONLY a Python list. Example: ["Concept1", "Concept2"]
            No explanation, no markdown, just the list.
            """
            
            message = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                max_tokens=200,
                temperature=0.3
            )
            
            response_text = message.content[0].text.strip()
            
            import ast
            concepts = ast.literal_eval(response_text)
            
            if isinstance(concepts, list) and concepts:
                return concepts
            return [concept]
        
        except Exception as e:
            self.logger.error(f"Concept extraction error: {str(e)}")
            return [concept]
    
    def _generate_wikipedia_resources(
        self, concepts: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate Wikipedia search resources.
        
        Wikipedia covers EVERYTHING from class 2 maths to PhD-level research.
        Links never break because they're search URLs.
        
        Args:
            concepts: Extracted learning concepts
        
        Returns:
            Wikipedia resource links
        """
        resources: List[Dict[str, Any]] = []
        
        try:
            for concept in concepts[:3]:
                search_query = quote(concept)
                
                resources.append({
                    "type": "reference",
                    "title": f"Wikipedia - {concept}",
                    "url": f"https://en.wikipedia.org/wiki/Special:Search?search={search_query}&go=Go",
                    "description": "Comprehensive encyclopedia covering all topics from basics to advanced",
                    "icon": "📖",
                    "source": "Wikipedia"
                })
        
        except Exception as e:
            self.logger.error(f"Wikipedia resource generation error: {str(e)}")
        
        return resources
    
    def _generate_youtube_resources(
        self, concepts: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate YouTube search resources.
        
        Returns fresh search URLs - never outdated or broken.
        Always shows latest, highest-rated videos.
        
        Args:
            concepts: Learning concepts
        
        Returns:
            YouTube search links
        """
        resources: List[Dict[str, Any]] = []
        
        try:
            for concept in concepts[:3]:
                search_query = quote(f"{concept} tutorial")
                
                resources.append({
                    "type": "video",
                    "title": f"YouTube - {concept} Tutorial",
                    "url": f"https://www.youtube.com/results?search_query={search_query}",
                    "description": "Video tutorials - from basics to advanced concepts",
                    "icon": "▶️",
                    "source": "YouTube"
                })
                
                advanced_query = quote(f"{concept} advanced in-depth")
                resources.append({
                    "type": "video",
                    "title": f"YouTube - {concept} (Advanced)",
                    "url": f"https://www.youtube.com/results?search_query={advanced_query}",
                    "description": "Deep-dive and advanced video tutorials",
                    "icon": "▶️",
                    "source": "YouTube"
                })
        
        except Exception as e:
            self.logger.error(f"YouTube resource generation error: {str(e)}")
        
        return resources
    
    def _generate_github_resources(
        self, concepts: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate GitHub search resources for code examples.
        
        Find open-source projects, implementations, and learning repositories.
        
        Args:
            concepts: Learning concepts
        
        Returns:
            GitHub search links
        """
        resources: List[Dict[str, Any]] = []
        
        try:
            for concept in concepts[:2]:
                search_query = quote(concept)
                
                resources.append({
                    "type": "code",
                    "title": f"GitHub - {concept} (Code Examples)",
                    "url": f"https://github.com/search?q={search_query}+language:python&type=repositories&sort=stars",
                    "description": "Open-source implementations and learning projects (Python)",
                    "icon": "💻",
                    "source": "GitHub"
                })
                
                resources.append({
                    "type": "code",
                    "title": f"GitHub - {concept} (All Languages)",
                    "url": f"https://github.com/search?q={search_query}&type=repositories&sort=stars",
                    "description": "Code examples in all programming languages",
                    "icon": "💻",
                    "source": "GitHub"
                })
        
        except Exception as e:
            self.logger.error(f"GitHub resource generation error: {str(e)}")
        
        return resources
    
    def _generate_devto_resources(
        self, concepts: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate Dev.to search resources for community tutorials.
        
        Community-written, practical tutorials and guides.
        
        Args:
            concepts: Learning concepts
        
        Returns:
            Dev.to search links
        """
        resources: List[Dict[str, Any]] = []
        
        try:
            for concept in concepts[:2]:
                search_query = quote(concept)
                
                resources.append({
                    "type": "tutorial",
                    "title": f"Dev.to - {concept} Tutorial",
                    "url": f"https://dev.to/search?q={search_query}",
                    "description": "Community-written practical tutorials and guides",
                    "icon": "📝",
                    "source": "Dev.to"
                })
        
        except Exception as e:
            self.logger.error(f"Dev.to resource generation error: {str(e)}")
        
        return resources
    
    def _generate_documentation_resources(
        self, concepts: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate links to official documentation and reference materials.
        
        Covers programming languages, frameworks, libraries, scientific concepts.
        
        Args:
            concepts: Learning concepts
        
        Returns:
            Documentation links
        """
        resources: List[Dict[str, Any]] = []
        
        documentation_map: Dict[str, Dict[str, str]] = {
            "Python": {
                "title": "Python Official Documentation",
                "url": "https://docs.python.org/3/",
                "description": "Official Python language specification"
            },
            "JavaScript": {
                "title": "MDN Web Docs - JavaScript",
                "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
                "description": "JavaScript reference and guides"
            },
            "Java": {
                "title": "Java Official Documentation",
                "url": "https://docs.oracle.com/javase/",
                "description": "Java language and API reference"
            },
            "React": {
                "title": "React Official Documentation",
                "url": "https://react.dev/",
                "description": "React API and architecture guide"
            },
            "Vue": {
                "title": "Vue.js Documentation",
                "url": "https://vuejs.org/guide/introduction.html",
                "description": "Vue framework guide"
            },
            "Django": {
                "title": "Django Documentation",
                "url": "https://docs.djangoproject.com/",
                "description": "Django web framework"
            },
            "Machine Learning": {
                "title": "Scikit-learn Documentation",
                "url": "https://scikit-learn.org/stable/",
                "description": "ML algorithms and models"
            },
            "TensorFlow": {
                "title": "TensorFlow Documentation",
                "url": "https://www.tensorflow.org/learn",
                "description": "Deep learning framework"
            },
            "PyTorch": {
                "title": "PyTorch Documentation",
                "url": "https://pytorch.org/docs/stable/index.html",
                "description": "PyTorch deep learning framework"
            },
            "SQL": {
                "title": "SQL Tutorial - W3Schools",
                "url": "https://www.w3schools.com/sql/",
                "description": "SQL syntax and database concepts"
            },
            "MongoDB": {
                "title": "MongoDB Documentation",
                "url": "https://docs.mongodb.com/manual/",
                "description": "MongoDB NoSQL database"
            },
            "Mathematics": {
                "title": "Khan Academy - Mathematics",
                "url": "https://www.khanacademy.org/math",
                "description": "Math from basic to advanced"
            },
            "Physics": {
                "title": "Khan Academy - Physics",
                "url": "https://www.khanacademy.org/science",
                "description": "Physics concepts explained"
            },
            "Chemistry": {
                "title": "Khan Academy - Chemistry",
                "url": "https://www.khanacademy.org/science/chemistry",
                "description": "Chemistry fundamentals"
            },
            "Data Structures": {
                "title": "GeeksforGeeks - DSA",
                "url": "https://www.geeksforgeeks.org/data-structures/",
                "description": "DSA tutorials and implementations"
            },
            "Algorithms": {
                "title": "GeeksforGeeks - Algorithms",
                "url": "https://www.geeksforgeeks.org/fundamentals-of-algorithms/",
                "description": "Algorithm concepts and implementations"
            }
        }
        
        try:
            for concept in concepts:
                if concept in documentation_map:
                    doc = documentation_map[concept]
                    resources.append({
                        "type": "documentation",
                        "title": doc["title"],
                        "url": doc["url"],
                        "description": doc["description"],
                        "icon": "📚",
                        "source": "Official Docs"
                    })
        
        except Exception as e:
            self.logger.error(f"Documentation resource error: {str(e)}")
        
        return resources
