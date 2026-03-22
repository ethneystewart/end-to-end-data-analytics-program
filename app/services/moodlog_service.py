import logging

import psycopg2
from database.db import cursor, conn

logger = logging.getLogger("uvicorn.error")

def create_moodlog(date, sleepHours, energyLevels, activities, tags, user_id):
    try:
        cursor.execute(
            """
            INSERT INTO moodlog (date, sleepHours, energyLevel, activities, tags, user_id)
            VALUES (%s,%s,%s,%s,%s,%s)
            RETURNING *
            """,
            (date, sleepHours, energyLevels, activities, tags, user_id)
        )

        moodlog = cursor.fetchone()
        conn.commit()


    except psycopg2.Error as e:
        conn.rollback() 
        logger.error("Unable to create mood log for user_id=%s: %s", user_id, e, exc_info=True)
        raise
    
    return moodlog
  


def get_moodlogs():
    try:
        cursor.execute("SELECT * FROM moodlog")
        return cursor.fetchall()
    except psycopg2.Error:
        logger.exception("Database error while fetching mood logs.")
        raise
