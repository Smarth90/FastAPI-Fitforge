from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from backend.db.base import Base
from sqlalchemy.types import JSON
from sqlalchemy.sql import func
from sqlalchemy import Enum

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, index = True, nullable = False)
    hashed_password = Column(String, nullable = False)
    is_active = Column(Boolean, default = True)

    created_at = Column(DateTime(timezone = True), server_default = func.now())

    profile = relationship(
    "UserProfile", 
    back_populates = "user", 
    uselist = False,
    cascade = "all, delete-orphan"
    )

    workout_prefernces = relationship(
    "WorkoutPreferences",
    back_populates = "user",
    uselist = False,
    cascade = "all, delete-orphan"
    )

    diet_preferences = relationship(
    "DietPreferences",
    back_populates = "user",
    uselist = False,
    cascade = "all, delete-orphan"
    )

class UserProfile(Base):
    __tablename__ = "UserProfiles"
    id = Column(Integer, primary_key = True, index = True)
    gender = Column(String)
    user_id = Column(Integer, ForeignKey("Users.id"), unique = True, nullable = False)
    age = Column(Integer, nullable = False)
    weight_kg = Column(Float)
    height_ft = Column(Integer)
    height_in = Column(Integer)

    user = relationship("User", back_populates = "profile")
    plans = relationship("PlanHistory", back_populates= "user")

class WorkoutPreferences(Base):
    __tablename__ = "WorkoutPreferences"
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("Users.id"), unique = True)
    fitness_level = Column(String)
    goal = Column(String)
    days_per_week = Column(Integer)
    workout_duration = Column(String)
    equipment = Column(String)
    workout_types = Column(String)
    rest_days = Column(String)

    user = relationship("User", back_populates = "workout_prefernces")

class DietPreferences(Base):
    __tablename__ = "DietPreferences"
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("Users.id"), unique = True)
    diet_type = Column(String)
    cuisine = Column(String)
    allergies = Column(String)
    dislikes = Column(String)

    user = relationship("User", back_populates = "diet_preferences")

# id
# user_id
# plan_type
# plan_json
# created_at
class PlanHistory(Base):
    __tablename__ = "plan_history"
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_type = Column(Enum("workout", "diet", name="plan_type"))
    plan_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", backref="plan_history")