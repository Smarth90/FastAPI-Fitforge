from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.rag.chain import rag_answer
from backend.db.base import Base
from backend.db.session import engine
from backend.db.models import User, UserProfile, WorkoutPreferences, DietPreferences
from backend.db import models
from backend.api.profile import router as profile_router
from backend.api.auth import router as auth_router
from backend.api.workout import router as workout_router
from backend.core.dependencies import get_db, get_current_user
from backend.api.diet import router as diet_router


Base.metadata.create_all(bind=engine)
app = FastAPI(
    title= "FitForge API",
    description= "API for FitForge, your personal fitness assistant.",
    version= "1.0.0"
)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(workout_router)
app.include_router(diet_router)

class RAGRequest(BaseModel):
    question: str
    k: int = 4

class RAGResponse(BaseModel):
    answer: str


@app.get("/Active", tags=["Active Check"])
def health_check():
    return {"status": "FitForge API is active and running!"}

@app.post("/rag", response_model=RAGResponse, tags=["RAG"])
def rag_endpoint(request: RAGRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter_by(user_id = current_user.id).first()
    workout = db.query(WorkoutPreferences).filter_by(user_id = current_user.id).first()
    diet = db.query(DietPreferences).filter_by(user_id = current_user.id).first()
    answer = rag_answer(request.question, k = request.k)
    return {"answer": answer}