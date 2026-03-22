import logging

import psycopg2
from database.db import cursor, conn

logger = logging.getLogger("uvicorn.error")

def create_mood(mood, sentiment, moodlog_id):
    try:
        cursor.execute(
            """
            INSERT INTO mood (mood, sentiment, moodlog_id)
            VALUES (%s,%s,%s)
            RETURNING *
            """,
            (mood, sentiment, moodlog_id)
        )
        mood = cursor.fetchone()
        conn.commit()

        return mood
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(
            "Unable to create mood for moodlog_id=%s: %s",
            moodlog_id,
            e,
            exc_info=True,
        )
        raise

def get_moods():
    try:
        cursor.execute("SELECT * FROM mood")
        return cursor.fetchall()
    except psycopg2.Error:
        logger.exception("Database error while fetching moods.")
        raise
