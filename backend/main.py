from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag.chain import rag_answer
from backend.db.base import Base
from backend.db.session import engine
from backend.db.models import User, UserProfile, WorkoutPreference, DietPreference
from backend.db import models
from backend.api.profile import router as profile_router
from backend.api.auth import router as auth_router


Base.metadata.create_all(bind=engine)
app = FastAPI(
    title= "FitForge API",
    description= "API for FitForge, your personal fitness assistant.",
    version= "1.0.0"
)

app.include_router(auth_router)
app.include_router(profile_router)

class RAGRequest(BaseModel):
    question: str
    k: int = 4

class RAGResponse(BaseModel):
    answer: str


@app.get("/Active", tags=["Active Check"])
def health_check():
    return {"status": "FitForge API is active and running!"}

@app.post("/rag", response_model=RAGResponse, tags=["RAG"])
def rag_endpoint(request: RAGRequest):
    answer = rag_answer(request.question, k = request.k)
    return {"answer": answer}