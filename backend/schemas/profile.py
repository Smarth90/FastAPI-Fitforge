from pydantic import BaseModel

class UserProfileBase(BaseModel):
    gender: str
    age: int
    weight_kg: float
    height_ft: int
    height_in: int

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileOut(UserProfileBase):
    class Config:
        from_attribute = True