"""
FastAPI Application - Main Entry Point with Database
"""

from fastapi import FastAPI, HTTPException, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
import logging
import json
from sqlalchemy.orm import Session

from .config import settings
from .agents.orchestrator import AgentOrchestrator
from .db import init_db, get_db, QuestionCRUD, ResponseCRUD, ProgressCRUD


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize orchestrator lazily
orchestrator = None

def get_orchestrator():
    global orchestrator
    if orchestrator is None:
        orchestrator = AgentOrchestrator()
    return orchestrator


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    logger.info("🚀 Starting Guided Learning AI Server")
    # Initialize database
    init_db()
    logger.info("✅ Database initialized")
    yield
    logger.info("🛑 Shutting down server")


# Create FastAPI app
app = FastAPI(
    title="Guided Learning AI",
    description="AI-powered learning companion that guides students through homework",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/")
async def root():
    """Health check / Root endpoint"""
    return {
        "message": "Guided Learning AI Server",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.environment
    }


@app.post("/ask")
async def ask_question(request: dict, db: Session = Depends(get_db)):
    """
    Main endpoint: Student asks a question
    Saves question and response to database
    
    Request body:
    {
        "question": "How do I build a REST API?",
        "user_id": "user123",
        "context": "I'm new to Python"
    }
    """
    try:
        question = request.get("question", "")
        user_id = request.get("user_id", "anonymous")
        
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        logger.info(f"User {user_id} asked: {question}")
        
        # Get orchestrator and run all agents
        orch = get_orchestrator()
        result = await orch.orchestrate({
            "question": question,
            "user_id": user_id,
            "context": request.get("context", "")
        })
        
        if result.get("success"):
            # Extract data
            concept = result.get("summary", {}).get("concept", "General")
            difficulty = result.get("summary", {}).get("difficulty_level", "beginner")
            
            # Save question to database
            db_question = QuestionCRUD.create_question(
                db=db,
                user_id=user_id,
                question=question,
                concept=concept,
                difficulty_level=difficulty,
                context=request.get("context")
            )
            
            # Save response to database
            db_response = ResponseCRUD.create_response(
                db=db,
                question_id=db_question.id,
                user_id=user_id,
                problem_analysis=result.get("agents", {}).get("problem_analysis"),
                resources=result.get("agents", {}).get("resources"),
                explanation=result.get("agents", {}).get("explanation"),
                guidance=result.get("agents", {}).get("guidance"),
                practice=result.get("agents", {}).get("practice")
            )
            
            # Update or create progress
            progress = ProgressCRUD.get_concept_progress(db, user_id, concept)
            if progress:
                ProgressCRUD.increment_times_asked(db, progress.id)
            else:
                ProgressCRUD.create_progress(db, user_id, db_question.id, concept)
            
            logger.info(f"Question {db_question.id} and response {db_response.id} saved to database")
        
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download-questions-pdf")
async def download_questions_pdf(request: dict):
    """
    Generate and download study questions as PDF
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib import colors
        from io import BytesIO
        from datetime import datetime
        
        concept = request.get("concept", "Untitled")
        difficulty = request.get("difficulty_level", "beginner")
        questions = request.get("questions", [])
        
        if not questions:
            raise HTTPException(status_code=400, detail="No questions provided")
        
        # Create PDF in memory
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#333333'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            spaceAfter=6,
            leading=14
        )
        
        # Content
        content = []
        
        # Title
        content.append(Paragraph(f"📚 {concept}", title_style))
        content.append(Paragraph(f"Study Questions | Difficulty: {difficulty.capitalize()}", styles['Normal']))
        content.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
        content.append(Spacer(1, 0.3*inch))
        
        # Questions
        for idx, question in enumerate(questions, 1):
            q_num = question.get('question_number', idx)
            importance = question.get('importance', '⭐ Important')
            difficulty_q = question.get('difficulty', 'beginner')
            
            # Question number and importance
            content.append(Paragraph(f"<b>Q{q_num}. {importance} [{difficulty_q.upper()}]</b>", heading_style))
            
            # Question text
            question_text = question.get('question', '')
            content.append(Paragraph(question_text, normal_style))
            
            # Answer
            answer_text = question.get('answer', '')
            content.append(Paragraph("<b>Answer:</b>", styles['Normal']))
            content.append(Paragraph(answer_text, normal_style))
            
            # Explanation
            explanation_text = question.get('explanation', '')
            content.append(Paragraph("<b>Explanation:</b>", styles['Normal']))
            content.append(Paragraph(explanation_text, normal_style))
            
            # Spacing between questions
            content.append(Spacer(1, 0.2*inch))
        
        # Build PDF
        doc.build(content)
        
        # Get PDF data
        pdf_buffer.seek(0)
        
        return StreamingResponse(
            iter([pdf_buffer.getvalue()]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={concept.replace(' ', '_')}_questions.pdf"}
        )
    
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/check-practice-answer")
async def check_practice_answer(request: dict):
    """
    Check if a practice answer is correct using LLM
    """
    try:
        problem = request.get("problem", "")
        user_answer = request.get("user_answer", "")
        expected_hint = request.get("expected_hint", "")
        concept = request.get("concept", "")
        difficulty = request.get("difficulty_level", "beginner")
        
        if not problem or not user_answer:
            raise HTTPException(status_code=400, detail="Problem and answer required")
        
        orch = get_orchestrator()
        
        # Simple prompt for evaluating answer
        prompt = f"""Evaluate this answer. Return ONLY JSON:

Problem: {problem}
Hint: {expected_hint}
Student Answer: {user_answer}

{{
  "correct": true or false,
  "feedback": "1-2 sentences feedback",
  "explanation": "short explanation"
}}"""
        
        response = orch.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=200
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Clean up markdown if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        response_text = response_text.strip()
        
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}, Got: {response_text}")
            result = {
                "correct": False,
                "feedback": "Could not evaluate. Try rewording.",
                "explanation": ""
            }
        
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        logger.error(f"Error checking answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/user/{user_id}/history")
async def get_user_history(user_id: str, db: Session = Depends(get_db)):
    """Get question history for a user with full response data"""
    try:
        questions = QuestionCRUD.get_user_questions(db, user_id, limit=50)
        
        history_data = []
        for question in questions:
            # Get the response for this question
            responses = ResponseCRUD.get_question_responses(db, question.id)
            response = responses[0] if responses else None
            
            # Build history item
            history_item = {
                "id": question.id,
                "question": question.question,
                "concept": question.concept,
                "difficulty_level": question.difficulty_level,
                "context": question.context,
                "created_at": question.created_at.isoformat(),
                "response_data": None
            }
            
            # Add full response data if exists
            if response:
                try:
                    history_item["response_data"] = {
                        "agents": {
                            "problem_analysis": json.loads(response.problem_analysis) if response.problem_analysis else {},
                            "resources": json.loads(response.resources) if response.resources else {},
                            "explanation": json.loads(response.explanation) if response.explanation else {},
                            "guidance": json.loads(response.guidance) if response.guidance else {},
                            "practice": json.loads(response.practice) if response.practice else {}
                        }
                    }
                except Exception as e:
                    logger.error(f"Error parsing response data: {str(e)}")
            
            history_data.append(history_item)
        
        return {
            "success": True,
            "user_id": user_id,
            "total_questions": len(history_data),
            "questions": history_data
        }
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/user/{user_id}/progress")
async def get_user_progress(user_id: str, db: Session = Depends(get_db)):
    """Get learning progress for a user"""
    try:
        progress = ProgressCRUD.get_user_progress(db, user_id)
        return {
            "success": True,
            "user_id": user_id,
            "total_concepts": len(progress),
            "progress": progress
        }
    except Exception as e:
        logger.error(f"Error fetching progress: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/concept/{concept}/questions")
async def get_concept_questions(concept: str, db: Session = Depends(get_db)):
    """Get all questions for a concept"""
    try:
        questions = QuestionCRUD.get_concept_questions(db, concept)
        return {
            "success": True,
            "concept": concept,
            "total_questions": len(questions),
            "questions": questions
        }
    except Exception as e:
        logger.error(f"Error fetching concept questions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time agent updates
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            
            # Process message
            message = json.loads(data)
            orch = get_orchestrator()
            response = await orch.orchestrate(message)
            
            # Send response
            await websocket.send_json({
                "success": True,
                "data": response
            })
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=1000)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )