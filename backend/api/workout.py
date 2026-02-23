from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import SessionLocal
from backend.db.models import WorkoutPreferences
from backend.core.dependencies import get_current_user
from backend.db.models import User
from backend.schemas.workout import UserWorkoutPrefernces, UserWorkoutProfileOut


router = APIRouter(prefix="/workout", tags = ["Workout"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserWorkoutProfileOut)
def create_or_update_workout_preferences(payload: UserWorkoutPrefernces, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    profile = db.query(WorkoutPreferences).filter_by(user_id = user_id).first()