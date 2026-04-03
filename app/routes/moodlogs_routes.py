import logging

import psycopg2
from fastapi import APIRouter, HTTPException
from app.models.request_models import MoodLogCreate
from app.services.moodlog_service import create_moodlog, get_moodlogs

router = APIRouter(prefix="/moodlogs", tags=["MoodLogs"])
logger = logging.getLogger("uvicorn.error")


@router.get("/")
def get_moodlogs_route():
    try:
        return get_moodlogs()
    except psycopg2.Error:
        logger.exception("Database error while getting mood logs.")
        raise HTTPException(status_code=500, detail="Database error while getting mood logs.")


@router.post("/")
def create_moodlog_route(log: MoodLogCreate):
    try: #success
        return create_moodlog(
            log.date,
            log.sleepHours,
            log.energyLevels,
            log.activities,
            log.tags,
            log.user_id
        )
    except psycopg2.errors.ForeignKeyViolation: #Foreign Key violation database level error catch 
        logger.warning("Invalid user_id for moodlog create: user_id=%s", log.user_id)
        raise HTTPException( #instead of crashing 
            status_code=400,
            detail="Invalid user_id: user does not exist."
        )
        

    except psycopg2.Error: #catches the rest of the errors 
        logger.exception("Database error while creating mood log.")
        raise HTTPException(
            status_code=500,
            detail="Database error while creating mood log."
        )
