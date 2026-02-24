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

    if profile:
        profile.fitness_level = payload.fitness_level
        profile.goal = payload.goal
        profile.days_per_week = payload.days_per_week
        profile.workout_duration = payload.workout_duration
        profile.equipment = payload.equipment
        profile.workout_types = payload.workout_types
        profile.rest_days = payload.rest_days  
    else:
        profile = WorkoutPreferences(
            user_id = user_id,
            fitness_level = payload.fitness_level,
            goal = payload.goal,
            days_per_week = payload.days_per_week,
            workout_duration = payload.workout_duration,
            equipment = payload.equipment,
            workout_types = payload.workout_types,
            rest_days = payload.rest_days
        )
        db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

