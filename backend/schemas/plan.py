from pydantic import BaseModel
from datetime import datetime
class PlanCreate(BaseModel):
    plan_type: str
    plan_json: dict

class PlanOut(PlanCreate):
    id : int 

    created_at : datetime

    class Config:
        from_attributes = True