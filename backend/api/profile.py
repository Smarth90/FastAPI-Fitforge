from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import SessionLocal
from backend.db.models import UserProfile
from backend.schemas.profile import UserProfileCreate, UserProfileOut


router = APIRouter(prefix="/profile", tags=["Profile"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserProfileOut)
def create_or_update_profile(payload: UserProfileCreate, db: Session = Depends(get_db)):
    user_id = 1  

    profile = db.query(UserProfile).filter_by(user_id=user_id).first()

    if profile:
        profile.gender = payload.gender
        profile.age = payload.age
        profile.weight_kg = payload.weight_kg
        profile.height_ft = payload.height_ft
        profile.height_in = payload.height_in
    else:
        profile = UserProfile(
            user_id=user_id,
            gender=payload.gender,
            age=payload.age,
            weight_kg=payload.weight_kg,
            height_ft=payload.height_ft,
            height_in=payload.height_in,
        )
        db.add(profile)

    db.commit()
    db.refresh(profile)

    return profile


@router.get("/", response_model = UserProfileOut)
def get_profile(db: Session = Depends(get_db)):
    user_id = 1
    profile = db.query(UserProfile).filter_by(user_id = user_id).first()

    if not profile:
        raise HTTPException(status_code = 404, detail = "Profile not found")
    return profile
