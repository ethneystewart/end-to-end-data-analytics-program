from pydantic import BaseModel
from datetime import date
from typing import List

#defines what incoming API requests must look like 

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: str

class MoodLogCreate(BaseModel):
    date: date
    sleepHours: int
    energyLevels: str
    activities: list[str]
    tags: list[str]
    user_id: int

class MoodCreate(BaseModel):
    mood: str
    sentiment: str
    moodlog_id: int


class ReflectionCreate(BaseModel):
    reflection: str
    moodlog_id: int