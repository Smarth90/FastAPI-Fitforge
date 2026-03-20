from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import SessionLocal
from backend.core.dependencies import get_current_user, get_db
from backend.db.models import (
    User,
    UserProfile,
    WorkoutPreferences,
    DietPreferences,
    PlanHistory
)
from backend.schemas.plan import PlanOut
from backend.rag.chain import rag_answer, rag_generate_plan

router = APIRouter(prefix = "/generate", tags = ["Profile"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PlanOut)
def generate_workout_plan(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    profile = db.query(UserProfile).filter_by(user_id=user_id).first()
    workout = db.query(WorkoutPreferences).filter_by(user_id = user_id).first()
    diet = db.query(DietPreferences).filter_by(user_id = user_id).first()

    if not profile or not workout:
        raise HTTPException(status_code= 400, detail= "Profile and workout preferences required first")
    context = {
        "profile": {
            "age": profile.age,
            "gender": profile.gender,
            "weight": profile.weight_kg,
            "height_ft": profile.height_ft,
            "height_in": profile.height_in,
        },
        "workout_preferences": {
            "fitness_level": workout.fitness_level,
            "goal": workout.goal,
            "days_per_week": workout.days_per_week,
            "duration": workout.workout_duration,
            "equipment": workout.equipment,
            "types": workout.workout_types,
        },
        "diet_preferences": {
            "diet_type": diet.diet_type if diet else None,
            "cuisine": diet.cuisine if diet else None,
            "allergies": diet.allergies if diet else None,
        },
    }

    generated_plan = rag_generate_plan(context)

    plan_entry = PlanHistory(
        user_id=current_user.id,
        plan_type="workout",
        plan_json=generated_plan
    )

    db.add(plan_entry)
    db.commit()
    db.refresh(plan_entry)

    return plan_entry

@router.get("/history", response_model=list[PlanOut])
def get_plan_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    plans = (
        db.query(PlanHistory)
        .filter_by(user_id=current_user.id)
        .order_by(PlanHistory.created_at.desc())
        .all()
    )

    return plans
