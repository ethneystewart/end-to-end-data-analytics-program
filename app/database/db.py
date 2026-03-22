import os
import psycopg2

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "db"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()