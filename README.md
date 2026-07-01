![Guided_learning_Ai](https://socialify.git.ci/harivarshney/guided_learning_ai/image?description=1&font=Rokkitt&language=1&name=1&owner=1&pattern=Circuit+Board&theme=Dark)


<div align="center">

# 🎓 Guided Learning AI

### An intelligent multi-agent learning companion that doesn't just answer — it teaches.

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)](https://www.python.org/)
[![React.js](https://img.shields.io/badge/React.js-61DAFB?style=flat-square&logo=react)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Railway-4169E1?style=flat-square&logo=postgresql)](https://railway.app/)
[![Groq](https://img.shields.io/badge/Groq-llama--3.3--70b-orange?style=flat-square)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 💡 The Idea

Most AI tools give students the answer. **Guided Learning AI gives them understanding.**

Instead of a single prompt-response loop, this project runs a **5-agent AI pipeline** that breaks a question down the way a great tutor would — understanding what you're actually stuck on, explaining the concept from first principles, walking you through it step-by-step *without* handing you the solution, and then testing you with curated practice questions.

Built as a full-stack, production-shaped system: FastAPI backend, React frontend, PostgreSQL persistence, and a real multi-agent orchestration layer — not just a wrapper around a single LLM call.

---

## ✨ What It Actually Does

| | |
|---|---|
| 🧠 **Problem Understanding Agent** | Figures out exactly what the student is confused about before responding |
| 📖 **Concept Explainer Agent** | Deep, structured explanations — history, first principles, real-world use, comparisons, common mistakes |
| 🗺️ **Guided Solution Agent** | 5-step scaffolded guidance with hints and thinking prompts — guides *toward* the answer, never gives it away |
| 🔗 **Resource Finder Agent** | Curated Wikipedia, YouTube, GitHub, and Dev.to links tailored to the question |
| 📝 **Question Generator Agent** | 20 ranked study questions (⭐ Important / ⭐⭐ Very Important) with full answers and explanations, downloadable as a PDF |

All five run per question, and every response is persisted — so a student's learning history and concept mastery build up over time.

---

## 🖼️ Preview

**Ask anything → get a full guided learning session across 5 tabs:**

```
Problem Analysis  →  Resources  →  Deep Explanation  →  Step-by-Step Guidance  →  Study Questions
```

Every past session is saved and revisitable from the **History** page, and overall concept mastery is tracked on the **Progress** dashboard.

---

## 🏗️ Architecture

```
                          ┌─────────────────────┐
                          │   Student Question   │
                          └──────────┬───────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │        Orchestrator Agent         │
                    └────────────────┬────────────────┘
                                     │
        ┌───────────────┬───────────┼───────────┬───────────────┐
        ▼               ▼           ▼           ▼               ▼
  Problem Under-   Concept Ex-  Resource     Guided Sol-   Question Gen-
  standing Agent   plainer Agent Finder Agent ution Agent   erator Agent
        │               │           │           │               │
        └───────────────┴───────────┼───────────┴───────────────┘
                                     ▼
                        ┌─────────────────────────┐
                        │   PostgreSQL (Railway)   │
                        │  questions · progress    │
                        │       · users            │
                        └────────────┬────────────┘
                                     ▼
                        ┌─────────────────────────┐
                        │   React Tabbed UI        │
                        │  + PDF export + History  │
                        └─────────────────────────┘
```

Full database structure documented in [`DATABASE_SCHEMA.md`](./DATABASE_SCHEMA.md).

---

## 🛠️ Tech Stack

**Backend**
- FastAPI (Python 3.12)
- SQLAlchemy ORM + PostgreSQL (Railway)
- Groq API — `llama-3.3-70b-versatile`
- ReportLab (PDF generation)

**Frontend**
- React.js
- Component-based tabbed UI with custom modals
- Fetch-based API client

**Infra**
- Railway (PostgreSQL + backend hosting)
- Vercel-ready frontend build

---

## 🚀 Quick Start

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
```

Create `backend/.env`:
```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=your_railway_postgres_url
```

```bash
python -m uvicorn app.main:app --reload
```
Runs at `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
```

Create `frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:8000
```

```bash
npm start
```
Runs at `http://localhost:3000`

---

## 📡 Key API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ask` | Runs the full 5-agent pipeline on a question |
| `POST` | `/download-questions-pdf` | Generates a downloadable PDF of the 20 study questions |
| `GET` | `/user/{user_id}/history` | Full history of past questions & responses |
| `GET` | `/user/{user_id}/progress` | Per-concept understanding & mastery tracking |
| `GET` | `/concept/{concept}/questions` | Fetch questions by concept |

---

## 📂 Project Structure

```
guided-learning-ai/
├── backend/
│   └── app/
│       ├── agents/          # 5 specialized AI agents + orchestrator
│       ├── db/               # SQLAlchemy models, schemas, CRUD
│       ├── main.py           # FastAPI entrypoint
│       └── config.py
├── frontend/
│   └── src/
│       ├── components/       # Navbar, modals, response display
│       ├── pages/            # Home, History, Progress
│       └── api/               # API client
├── DATABASE_SCHEMA.md
└── README.md
```

---

## 🎯 Why This Project

This isn't a chatbot wrapper. It's an exercise in **agent orchestration, structured LLM output, and product thinking** — designing a system where each agent has a narrow, well-defined job, the outputs compose into something coherent, and the UX actually reflects how people learn (understand → explain → guide → practice) rather than just "ask and receive."

---

## 👨‍💻 Author

**Hari Varshney**
Final-year B.Tech, AI/ML 

---

## 📄 License

MIT — see [LICENSE](./LICENSE)

</div>
