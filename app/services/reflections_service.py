import logging

import psycopg2
from database.db import cursor, conn

logger = logging.getLogger("uvicorn.error")

def create_reflection(reflection, moodlog_id):
    try:
        cursor.execute(
            """
            INSERT INTO reflection (moodlog_id, reflection)
            VALUES (%s, %s)
            RETURNING *
            """,
            (moodlog_id, reflection)
        )

        reflection = cursor.fetchone()
        conn.commit()

        return reflection
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(
            "Unable to create reflection for moodlog_id=%s: %s",
            moodlog_id,
            e,
            exc_info=True,
        )
        raise

def get_reflections(moodlog_id):
    try:
        cursor.execute(
            """
            SELECT * FROM reflection
            WHERE moodlog_id = %s
            """,
            (moodlog_id,)
        )

        return cursor.fetchall()
    except psycopg2.Error:
        logger.exception("Database error while fetching reflections for moodlog_id=%s.", moodlog_id)
        raise
