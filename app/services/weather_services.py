import logging
from typing import Any, Dict, Optional

import requests
from psycopg2 import Error as Psycopg2Error
from psycopg2.extras import Json

from app.database.db import conn, cursor

logger = logging.getLogger("uvicorn.error")


def fetch_weather_raw(lat: float, lon: float) -> Dict[str, Any]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "apparent_temperature",
            "weather_code",
            "is_day",
            "precipitation",
            "wind_speed_10m",
        ],
        "timezone": "auto",
    }

    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error("Weather API request failed for lat=%s lon=%s: %s", lat, lon, e)
        raise

    raw_json = response.json()
    return raw_json


def save_weather_raw(moodlog_id: int, raw_payload: Dict[str, Any], source: str = "open-meteo") -> Optional[Dict[str, Any]]:
    try:
        cursor.execute(
            """
            INSERT INTO weather_raw (moodlog_id, source, raw_payload)
            VALUES (%s, %s, %s)
            ON CONFLICT (moodlog_id) DO UPDATE SET
                source = EXCLUDED.source,
                raw_payload = EXCLUDED.raw_payload,
                requested_at = now()
            RETURNING *
            """,
            (moodlog_id, source, Json(raw_payload)),
        )
        record = cursor.fetchone()
        conn.commit()
        logger.info("Saved raw weather for moodlog_id=%s", moodlog_id)
        return record
    except Psycopg2Error as exc:
        conn.rollback()
        logger.exception("Failed to save raw weather for moodlog_id=%s: %s", moodlog_id, exc)
        raise


def transform_weather_raw(moodlog_id: int) -> Optional[Dict[str, Any]]:
    cursor.execute(
        "SELECT raw_payload FROM weather_raw WHERE moodlog_id = %s",
        (moodlog_id,),
    )
    row = cursor.fetchone()
    if not row:
        logger.warning("No raw weather payload for moodlog_id=%s", moodlog_id)
        return None

    payload = row[0]
    current = payload.get("current") or payload.get("current_weather")
    if not current:
        logger.warning("Payload missing current weather for moodlog_id=%s", moodlog_id)
        return None

    return {
        "temperature_2m": current.get("temperature") or current.get("temperature_2m"),
        "apparent_temperature": current.get("apparent_temperature"),
        "weather_code": current.get("weathercode") or current.get("weather_code"),
        "is_day": current.get("is_day"),
        "precipitation": current.get("precipitation"),
        "wind_speed_10m": current.get("windspeed") or current.get("wind_speed_10m"),
    }


def save_weather_observation(moodlog_id: int, observation: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not observation:
        logger.warning("Skipping weather_observation insert for moodlog_id=%s because payload is empty", moodlog_id)
        return None

    try:
        cursor.execute(
            """
            INSERT INTO weather_observation (
                moodlog_id,
                temperature_2m,
                apparent_temperature,
                weather_code,
                is_day,
                precipitation,
                wind_speed_10m
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (moodlog_id) DO UPDATE SET
                temperature_2m = EXCLUDED.temperature_2m,
                apparent_temperature = EXCLUDED.apparent_temperature,
                weather_code = EXCLUDED.weather_code,
                is_day = EXCLUDED.is_day,
                precipitation = EXCLUDED.precipitation,
                wind_speed_10m = EXCLUDED.wind_speed_10m
            RETURNING *
            """,
            (
                moodlog_id,
                observation.get("temperature_2m"),
                observation.get("apparent_temperature"),
                observation.get("weather_code"),
                observation.get("is_day"),
                observation.get("precipitation"),
                observation.get("wind_speed_10m"),
            ),
        )
        record = cursor.fetchone()
        conn.commit()
        logger.info("Saved transformed weather for moodlog_id=%s", moodlog_id)
        return record
    except Psycopg2Error as exc:
        conn.rollback()
        logger.exception("Failed to save transformed weather for moodlog_id=%s: %s", moodlog_id, exc)
        raise
