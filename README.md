# ProjectMentor AI

ProjectMentor AI turns final-year student skills and interests into practical project ideas, then expands a selected idea into a full build roadmap, technical architecture, mentor chat, and refinement loop.

## Problem and solution

Students often struggle to turn broad interests into a feasible project. This MVP captures real skills and constraints, generates structured ideas with Gemini, and supplies a path from MVP to viva. It remains fully demoable without credentials through Demo Mode.

## Stack and architecture

- React + Vite + JavaScript + custom CSS + Lucide icons
- Python + FastAPI + Pydantic REST API
- Google Gemini via official `google-genai` SDK, model `gemini-3.8-flash`

`React browser → FastAPI REST API → Gemini or deterministic Demo Mode`

The Gemini key is read only by FastAPI. It is never sent to React or rendered in the UI.

## Setup

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend
uvicorn main:app --reload --port 8000
```

Copy `.env.example` to `.env` at the project root and optionally set:

```env
GEMINI_API_KEY=your_key_here
```

If absent or unavailable, the API automatically uses complete Demo Mode.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Vite calls FastAPI at `http://localhost:8000`; use `VITE_API_URL` when deployed elsewhere.

## API

- `POST /api/projects/generate` — structured 3–5 project ideas
- `POST /api/projects/explore` — selected project mentor plan
- `POST /api/projects/refine` — revised structured plan
- `POST /api/mentor/chat` — project-aware mentor response
- `GET /api/health` — API status and mode

## Hackathon demo

1. Generate ideas from skills and interests.
2. Explore a project card.
3. Open its roadmap and architecture diagram.
4. Ask about deployment or the viva.
5. Refine the scope to be cheaper, beginner-friendly, or more innovative.

## Deployment

Deploy `frontend/` to Vercel/Netlify and `backend/` to Render/Railway. Configure `GEMINI_API_KEY` only on the backend, set `VITE_API_URL` in the frontend deployment, and add the deployed frontend origin to CORS in `backend/main.py`.
