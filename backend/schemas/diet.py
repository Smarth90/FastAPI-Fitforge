from pydantic import BaseModel

class DietBase(BaseModel):
    diet_type: str
    cuisine: str
    allergies: str
    dislikes: str

    
class DietBaseCreate(DietBase):
    pass

class DietBaseOut(DietBase):
    class Config:
        from_attribute = True