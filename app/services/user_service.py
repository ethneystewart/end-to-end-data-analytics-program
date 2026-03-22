import logging

import psycopg2
from database.db import cursor, conn

logger = logging.getLogger("uvicorn.error")


def get_users():
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return users
    except psycopg2.Error:
        logger.exception("Database error while fetching users.")
        raise


def create_user(first_name, last_name, email):

    try:
        cursor.execute(
            """
            INSERT INTO users (firstName, lastName, email)
            VALUES (%s, %s, %s)
            RETURNING *
            """,
            (first_name, last_name, email)
        )

        user = cursor.fetchone()
        conn.commit()

        return user

    except psycopg2.Error as e:
        conn.rollback()
        logger.error("Unable to create user with email=%s: %s", email, e, exc_info=True)
        raise
