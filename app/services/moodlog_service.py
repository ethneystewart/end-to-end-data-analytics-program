import logging
import os

import psycopg2
from app.database.db import conn, cursor
from app.services.weather_services import (
    fetch_weather_raw,
    save_weather_raw,
    transform_weather_raw,
    save_weather_observation,
)

logger = logging.getLogger("uvicorn.error")


def create_moodlog(date, sleepHours, energyLevels, activities, tags, user_id):
    try:
        cursor.execute(
            """
            INSERT INTO moodlog (date, sleepHours, energyLevel, activities, tags, user_id)
            VALUES (%s,%s,%s,%s,%s,%s)
            RETURNING *
            """,
            (date, sleepHours, energyLevels, activities, tags, user_id),
        )

        moodlog = cursor.fetchone()
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(
            "Unable to create mood log for user_id=%s: %s", user_id, e, exc_info=True
        )
        raise

    moodlog_id = moodlog[0]
    # trigger weather pipeline add 
    _run_weather_pipeline(moodlog_id)
    return moodlog


def get_moodlogs():
    try:
        cursor.execute("SELECT * FROM moodlog")
        return cursor.fetchall()
    except psycopg2.Error:
        logger.exception("Database error while fetching mood logs.")
        raise

# get the coords from the environ file 
def _get_default_coords():
    lat = os.getenv("DEFAULT_LATITUDE") or "53.5461"
    lon = os.getenv("DEFAULT_LONGITUDE") or "-113.4938"
    return float(lat), float(lon)

#
def _run_weather_pipeline(moodlog_id: int):
    lat, lon = _get_default_coords()
    try:
        raw_payload = fetch_weather_raw(lat, lon) # extract 
        save_weather_raw(moodlog_id, raw_payload) # store
        observation = transform_weather_raw(moodlog_id) # transform
        save_weather_observation(moodlog_id, observation) # save 
    except Exception as exc:
        logger.warning(
            "Weather pipeline for moodlog_id=%s failed, continuing without weather: %s",
            moodlog_id,
            exc,
            exc_info=True,
        )
