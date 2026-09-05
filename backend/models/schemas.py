from typing import Literal
from pydantic import BaseModel, Field

class Profile(BaseModel):
    interests: str = Field(min_length=1, max_length=800)
    skills: str = Field(min_length=1, max_length=800)
    domain: str = "Open to anything"
    experience: Literal["Beginner", "Intermediate", "Advanced"] = "Intermediate"
    complexity: Literal["Simple", "Moderate", "Advanced"] = "Moderate"
    language: str = ""
    constraints: str = ""

class ProjectIdea(BaseModel):
    title: str; short_description: str; problem: str; solution: str; why_it_matters: str; difficulty: str
    innovation_score: int = Field(ge=1, le=10)
    estimated_time: str; recommended_stack: list[str]; target_users: str
class GenerateResponse(BaseModel): ideas: list[ProjectIdea]; demo_mode: bool; notice: str | None = None
class TechItem(BaseModel): category: str; technology: str; why: str
class Phase(BaseModel): phase: str; tasks: list[str]; output: str; time: str
class Entity(BaseModel): name: str; fields: str
class Risk(BaseModel): challenge: str; mitigation: str
class Features(BaseModel): mvp: list[str]; advanced: list[str]; future: list[str]
class DatabaseDesign(BaseModel): needed: bool; summary: str; entities: list[Entity] = []; relationships: str = ""
class AIComponent(BaseModel): applicable: bool; recommendation: str; dataset: str; approach: str; metrics: str
class ProjectPlan(BaseModel):
    title: str; problem_statement: str; proposed_solution: str; target_users: str; expected_outcome: str
    features: Features; tech_stack: list[TechItem]; roadmap: list[Phase]; architecture: list[str]
    database: DatabaseDesign; ai_ml: AIComponent; improvements: list[str]; risks: list[Risk]
class ExploreRequest(BaseModel): idea: ProjectIdea; profile: Profile
class RefineRequest(BaseModel): plan: ProjectPlan; instruction: str = Field(min_length=1, max_length=1000); profile: Profile | None = None
class PlanResponse(BaseModel): plan: ProjectPlan; demo_mode: bool; notice: str | None = None
class ChatRequest(BaseModel): plan: ProjectPlan; question: str = Field(min_length=1, max_length=1200)
class ChatResponse(BaseModel): answer: str; demo_mode: bool; notice: str | None = None
