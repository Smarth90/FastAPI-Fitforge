from pydantic import BaseModel
from typing import List,Optional

class Exercise(BaseModel):
    name: str
    sets : Optional[int] = None
    reps : Optional[str] = None
    duration_minutes : Optional[int] = None
    rest: Optional[str] = None

class DayPlan(BaseModel):
    focus: str
    exercises: List[Exercise]

class WeeklyWorkoutPlan(BaseModel):
    goal: str
    fitness_level: str
    weekly_plan: dict[str, DayPlan]