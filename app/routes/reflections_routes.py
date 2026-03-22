import logging

import psycopg2
from fastapi import APIRouter, HTTPException
from models.request_models import ReflectionCreate
from services.reflections_service import create_reflection, get_reflections

router = APIRouter(prefix="/reflection", tags=["Reflections"])
logger = logging.getLogger("uvicorn.error")


# create a new reflection
@router.post("/reflections")
def create_reflection_route(reflection: ReflectionCreate):
    try:
        return create_reflection(
            reflection.reflection,
            reflection.moodlog_id
        )
    except psycopg2.errors.ForeignKeyViolation:
        logger.warning(
            "Invalid moodlog_id for reflection create: moodlog_id=%s",
            reflection.moodlog_id,
        )
        raise HTTPException(status_code=400, detail="Invalid moodlog_id: moodlog does not exist.")
    except psycopg2.Error:
        logger.exception("Database error while creating reflection.")
        raise HTTPException(status_code=500, detail="Database error while creating reflection.")

#get reflections for a specific mood log
@router.get("/reflections/{moodlog_id}")
def get_reflections_route(moodlog_id: int):
    try:
        return get_reflections(moodlog_id)
    except psycopg2.Error:
        logger.exception("Database error while getting reflections for moodlog_id=%s.", moodlog_id)
        raise HTTPException(status_code=500, detail="Database error while getting reflections.")
