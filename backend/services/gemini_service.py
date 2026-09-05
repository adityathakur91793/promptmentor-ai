import json, os
from copy import deepcopy
from pathlib import Path
from dotenv import load_dotenv
from services.prompts import SYSTEM_PROMPT

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
MODEL = "gemini-3.8-flash"

def _schema(kind):
    s={"type":"string"}; ss={"type":"array","items":s}
    if kind=="ideas":
        p={"title":s,"short_description":s,"problem":s,"solution":s,"why_it_matters":s,"difficulty":s,"innovation_score":{"type":"integer"},"estimated_time":s,"recommended_stack":ss,"target_users":s}
        return {"type":"object","properties":{"ideas":{"type":"array","items":{"type":"object","properties":p,"required":list(p)}}},"required":["ideas"]}
    if kind=="chat": return {"type":"object","properties":{"answer":s},"required":["answer"]}
    feat={"type":"object","properties":{"mvp":ss,"advanced":ss,"future":ss},"required":["mvp","advanced","future"]}
    tech={"type":"object","properties":{"category":s,"technology":s,"why":s},"required":["category","technology","why"]}
    phase={"type":"object","properties":{"phase":s,"tasks":ss,"output":s,"time":s},"required":["phase","tasks","output","time"]}
    entity={"type":"object","properties":{"name":s,"fields":s},"required":["name","fields"]}
    db={"type":"object","properties":{"needed":{"type":"boolean"},"summary":s,"entities":{"type":"array","items":entity},"relationships":s},"required":["needed","summary","entities","relationships"]}
    ai={"type":"object","properties":{"applicable":{"type":"boolean"},"recommendation":s,"dataset":s,"approach":s,"metrics":s},"required":["applicable","recommendation","dataset","approach","metrics"]}
    risk={"type":"object","properties":{"challenge":s,"mitigation":s},"required":["challenge","mitigation"]}
    p={"title":s,"problem_statement":s,"proposed_solution":s,"target_users":s,"expected_outcome":s,"features":feat,"tech_stack":{"type":"array","items":tech},"roadmap":{"type":"array","items":phase},"architecture":ss,"database":db,"ai_ml":ai,"improvements":ss,"risks":{"type":"array","items":risk}}
    return {"type":"object","properties":p,"required":list(p)}

def _ask(prompt, kind):
    from google import genai
    from google.genai import types
    client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    result=client.models.generate_content(model=MODEL, contents=prompt, config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, response_mime_type="application/json", response_json_schema=_schema(kind), temperature=.65))
    return json.loads(result.text or "{}")

def _live(): return bool(os.getenv("GEMINI_API_KEY"))
def generate_ideas(profile):
    if _live():
        try:
            data=_ask(f"Generate exactly 4 practical final-year ideas for {json.dumps(profile)}.","ideas"); ideas=data.get("ideas",[])
            if len(ideas)>=3: return ideas[:5],False,None
            raise ValueError("incomplete ideas")
        except Exception as e: return demo_ideas(profile),True,f"Gemini unavailable; using complete Demo Mode ({type(e).__name__})."
    return demo_ideas(profile),True,None
def create_plan(idea,profile):
    if _live():
        try:
            plan=_ask(f"Create a detailed complete project mentor plan for {json.dumps(idea)}. Student profile: {json.dumps(profile)}. Use 8 roadmap phases.","plan")
            if plan.get("roadmap") and plan.get("features"): return plan,False,None
            raise ValueError("incomplete plan")
        except Exception as e: return demo_plan(idea),True,f"Gemini plan unavailable; using Demo Mode ({type(e).__name__})."
    return demo_plan(idea),True,None
def refine_plan(plan,instruction,profile):
    if _live():
        try:
            data=_ask(f"Refine this plan based on '{instruction}'. Keep it feasible for {json.dumps(profile)}. Plan: {json.dumps(plan)}","plan")
            if data.get("roadmap"): return data,False,None
            raise ValueError("incomplete plan")
        except Exception as e: return local_refine(plan,instruction),True,f"Gemini refinement unavailable; applied Demo Mode refinement ({type(e).__name__})."
    return local_refine(plan,instruction),True,None
def mentor_chat(plan,question):
    if _live():
        try:
            data=_ask(f"Answer specifically about this selected project: {json.dumps(plan)}\nStudent question: {question}","chat")
            if data.get("answer"): return data["answer"],False,None
            raise ValueError("empty answer")
        except Exception as e: return demo_answer(plan,question),True,f"Gemini mentor unavailable; using Demo Mode ({type(e).__name__})."
    return demo_answer(plan,question),True,None

def demo_ideas(p):
    lang=p.get("language") or "Python"; rows=[
    ("CampusPulse","A privacy-first campus issue reporting and resolution tracker.","Students cannot reliably report and follow up on maintenance and safety issues.","A guided report and status dashboard for visible accountability.","A campus can pilot it immediately with real feedback.","Moderate",8,"4–6 weeks",[lang,"React","FastAPI","PostgreSQL"],"Students, facilities teams, student council"),
    ("SkillSprint","An adaptive micro-learning planner that turns skill gaps into weekly challenges.","Students have resources but no focused, measurable practice plan.","A planner recommends short projects and tracks evidence of progress.","Useful to peers and demonstrates explainable recommendation logic.","Moderate",8,"5–7 weeks",[lang,"React","FastAPI","SQLite"],"Final-year students and mentors"),
    ("EcoRoute","A carbon-aware commute and campus travel planner.","Students cannot compare low-impact routes, costs, and travel time.","A route comparison experience with personal impact estimates.","Sustainability is relatable and the scope is very manageable.","Simple",7,"3–4 weeks",[lang,"React","FastAPI","Maps API (optional)"],"Campus commuters"),
    ("StudySignal","A study wellbeing check-in that spots overload patterns without diagnosing.","Students notice overload only after productivity and wellbeing drop.","A private check-in and trends dashboard with transparent suggestions.","Ethical, timely, and demonstrable without health claims.","Moderate",9,"4–6 weeks",[lang,"React","FastAPI","SQLite"],"University students and counsellors")]
    return [dict(zip(["title","short_description","problem","solution","why_it_matters","difficulty","innovation_score","estimated_time","recommended_stack","target_users"],x)) for x in rows]

def demo_plan(i):
    title=i["title"]
    phases=[("Phase 1 — Research & Requirements",["Interview 5 users","Write a success metric"],"Requirements and user flow","2–3 days"),("Phase 2 — Architecture",["Draw data flow","Define entities and APIs"],"Diagram and schema","1–2 days"),("Phase 3 — Environment Setup",["Create repository","Set up React and FastAPI"],"Runnable starter","1 day"),("Phase 4 — Core Development",["Build primary workflow","Persist records","Build dashboard"],"End-to-end MVP","10–14 days"),("Phase 5 — AI/ML Integration",["Add explainable rules","Test edge cases"],"Useful smart layer","3–4 days"),("Phase 6 — Testing",["Test validation","Run user test"],"Bug log and evidence","3 days"),("Phase 7 — Deployment",["Configure environment","Deploy and smoke test"],"Live demo URL","1 day"),("Phase 8 — Documentation & Presentation",["Write README","Prepare viva slides"],"Submission package","2–3 days")]
    return {"title":title,"problem_statement":i["problem"],"proposed_solution":i["solution"],"target_users":i["target_users"],"expected_outcome":"A strong, demoable MVP with a measurable impact story and maintainable codebase.","features":{"mvp":["Mobile-ready primary workflow","Create and view records with status","Dashboard with filters","Input validation"],"advanced":["Role-based admin workspace","Explainable priority rules","Notifications and exportable reports"],"future":["PWA mobile app","Institution integrations","Anonymised analytics"]},"tech_stack":[{"category":"Frontend","technology":"React + Vite","why":"Fast, responsive interface with reusable components."},{"category":"Backend","technology":"Python + FastAPI","why":"Typed REST APIs and an ideal Gemini integration boundary."},{"category":"Database","technology":"SQLite locally, PostgreSQL in production","why":"Low setup cost now, safe scaling later."},{"category":"AI / ML","technology":"Gemini API + explainable rules","why":"Adds useful intelligence without training risk."},{"category":"APIs","technology":"REST JSON API","why":"Keeps browser and provider credentials safely separated."},{"category":"Deployment","technology":"Vercel + Render","why":"Simple, reliable hackathon deployment."}],"roadmap":[{"phase":a,"tasks":b,"output":c,"time":d} for a,b,c,d in phases],"architecture":["Student","↓","React Frontend","↓","FastAPI REST Backend","↓","Gemini AI / Demo fallback","↓","Structured response"],"database":{"needed":True,"summary":"A small relational data model preserves user progress and powers the dashboard.","entities":[{"name":"users","fields":"id, name, role, created_at"},{"name":"records","fields":"id, user_id, title, description, status, priority"},{"name":"activity_log","fields":"id, record_id, action, timestamp"}],"relationships":"One user owns many records; each record has many activity events."},"ai_ml":{"applicable":True,"recommendation":"Use Gemini for guided suggestions and transparent rules for scoring.","dataset":"Start with consented pilot data or synthetic seed data; verify licences for public sources.","approach":"Validate input → generate suggestion → show rationale → request user confirmation.","metrics":"Completion rate, user satisfaction, and precision of priority labels."},"improvements":["Accessibility audit","Role-specific dashboards","CSV/PDF export","Audit history","Multilingual labels","Opt-in feedback","PWA support"],"risks":[{"challenge":"Feature creep","mitigation":"Freeze scope after the primary end-to-end flow works."},{"challenge":"Poor input quality","mitigation":"Use validation, examples, and review."},{"challenge":"Privacy concerns","mitigation":"Collect minimum data and anonymise demos."},{"challenge":"Deployment surprises","mitigation":"Deploy a thin vertical slice early."}]}
def local_refine(plan,instruction):
    p=deepcopy(plan); t=instruction.lower()
    if any(x in t for x in ["beginner","cheap","cost"]): p["features"]["mvp"]=p["features"]["mvp"][:3];p["improvements"].insert(0,"Keep it free-tier friendly with one-command setup.")
    if any(x in t for x in ["ai","innovative","unique"]): p["features"]["advanced"].insert(0,"Explainable AI-assisted suggestions with visible reasoning")
    if "hardware" in t:p["improvements"].insert(0,"Use browser forms and public APIs only—no hardware required.")
    p["expected_outcome"]+=f" Refined: {instruction}.";return p
def demo_answer(plan,q):
    q=q.lower();t=plan["title"]
    if "dataset" in q or "data" in q:return f"For {t}, begin with a small consented pilot dataset or synthetic seed records. Make a data dictionary, remove identifiers, and verify every public dataset licence before use."
    if "deploy" in q:return f"Deploy {t} as a thin vertical slice: host React on Vercel, FastAPI on Render, and add CORS only for your frontend URL. Test in incognito before the viva."
    if "viva" in q:return f"For your {t} viva, lead with the user problem, demo one end-to-end workflow, explain why React/FastAPI/Gemini were chosen, show your data model and a test result, then finish with honest future scope."
    return f"For {t}, make that a testable slice: define input and expected output, implement the simplest rule or API first, then add a test case. Keep it behind the core MVP workflow until it is reliable."
