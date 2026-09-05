import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import ChatRequest, ChatResponse, ExploreRequest, GenerateResponse, PlanResponse, Profile, RefineRequest
from services.gemini_service import create_plan, generate_ideas, mentor_chat, refine_plan

app = FastAPI(title="ProjectMentor AI API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@app.get("/api/health")
def health(): return {"status": "ok", "provider": "gemini", "demo_mode": not bool(os.getenv("GEMINI_API_KEY"))}
@app.post("/api/projects/generate", response_model=GenerateResponse)
def generate(profile: Profile):
    ideas, demo, notice = generate_ideas(profile.model_dump()); return GenerateResponse(ideas=ideas, demo_mode=demo, notice=notice)
@app.post("/api/projects/explore", response_model=PlanResponse)
def explore(request: ExploreRequest):
    plan, demo, notice = create_plan(request.idea.model_dump(), request.profile.model_dump()); return PlanResponse(plan=plan, demo_mode=demo, notice=notice)
@app.post("/api/projects/refine", response_model=PlanResponse)
def refine(request: RefineRequest):
    plan, demo, notice = refine_plan(request.plan.model_dump(), request.instruction, request.profile.model_dump() if request.profile else {}); return PlanResponse(plan=plan, demo_mode=demo, notice=notice)
@app.post("/api/mentor/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer, demo, notice = mentor_chat(request.plan.model_dump(), request.question); return ChatResponse(answer=answer, demo_mode=demo, notice=notice)
