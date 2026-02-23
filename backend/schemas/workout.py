from pydantic import BaseModel

class UserWorkoutBase(BaseModel):
    fitness_level: str
    goal: str
    days_per_week: int
    workout_duration: str
    equipment: str
    workout_types: str
    rest_days: str

class UserWorkoutPrefernces(UserWorkoutBase):
    pass

class UserWorkoutProfileOut(UserWorkoutBase):
    id: int
    class Config:
        from_attribute = True