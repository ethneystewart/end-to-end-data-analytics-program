import logging

import psycopg2
from fastapi import APIRouter, HTTPException
from models.request_models import MoodCreate
from services.mood_service import create_mood, get_moods

router = APIRouter(prefix="/mood", tags=["Moods"])
logger = logging.getLogger("uvicorn.error")

#get all moods 
@router.get("/moods")
def get_moods_route():
    try:
        return get_moods()
    except psycopg2.Error:
        logger.exception("Database error while getting moods.")
        raise HTTPException(status_code=500, detail="Database error while getting moods.")

#create a new mood 
@router.post("/moods")
def create_mood_route(mood: MoodCreate):
    try:
        return create_mood(
            mood.mood,
            mood.sentiment,
            mood.moodlog_id
        )
    except psycopg2.errors.ForeignKeyViolation:
        logger.warning("Invalid moodlog_id for mood create: moodlog_id=%s", mood.moodlog_id)
        raise HTTPException(status_code=400, detail="Invalid moodlog_id: moodlog does not exist.")
    except psycopg2.errors.InvalidTextRepresentation:
        logger.warning("Invalid mood enum value received: mood=%s", mood.mood)
        raise HTTPException(status_code=400, detail="Invalid mood value.")
    except psycopg2.Error:
        logger.exception("Database error while creating mood.")
        raise HTTPException(status_code=500, detail="Database error while creating mood.")
