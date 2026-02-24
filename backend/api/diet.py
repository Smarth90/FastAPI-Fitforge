from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import SessionLocal
from backend.db.models import WorkoutPreferences
from backend.core.dependencies import get_current_user
from backend.db.models import User
from backend.schemas.diet import DietBaseCreate, DietBaseOut
from backend.db.models import DietPreferences


router = APIRouter(prefix="/diet", tags = ["Diet"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DietBaseOut)
def create_or_update_diet_preferences(payload: DietBaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    profile = db.query(DietPreferences).filter_by(user_id = user_id).first()

    if profile:
        profile.diet_type = payload.diet_type
        profile.cuisine = payload.cuisine
        profile.allergies = payload.allergies
        profile.dislikes = payload.dislikes
    else:
        profile = DietPreferences(
            user_id = user_id,
            diet_type = payload.diet_type,
            cuisine = payload.cuisine,
            allergies = payload.allergies,
            dislikes = payload.dislikes
        )
        db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/", response_model = DietBaseOut)
def get_diet_preferences(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    profile = db.query(DietPreferences).filter_by(user_id = user_id).first()

    if not profile:
        raise HTTPException(status_code = 404, detail = "Diet preferences not found")
    return profile