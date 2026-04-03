import logging

import psycopg2
from fastapi import APIRouter, HTTPException
from app.models.request_models import UserCreate
from app.services.user_service import create_user, get_users

router = APIRouter(prefix="/users", tags=["Users"])
logger = logging.getLogger("uvicorn.error")


@router.get("/")
def get_users_route():
    try:
        return get_users()
    except psycopg2.Error:
        logger.exception("Database error while getting users.")
        raise HTTPException(status_code=500, detail="Database error while getting users.")


@router.post("/")
def create_user_route(user: UserCreate):
    try:
        return create_user(
            user.firstName,
            user.lastName,
            user.email
        )
    except psycopg2.errors.UniqueViolation:
        logger.warning("Duplicate email attempted: %s", user.email)
        raise HTTPException(status_code=400, detail="Email already exists.")
    except psycopg2.Error:
        logger.exception("Database error while creating user.")
        raise HTTPException(status_code=500, detail="Database error while creating user.")
