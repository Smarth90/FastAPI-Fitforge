from pydantic import BaseModel

class UserWorkoutBase(BaseModel):
    gender: str
    age: int
    weight_kg: float
    height_ft: int
    height_in: int

class UserWorkoutPrefernces(UserWorkoutBase):
    pass

class UserWorkoutProfileOut(UserWorkoutBase):
    class Config:
        from_attribute = True