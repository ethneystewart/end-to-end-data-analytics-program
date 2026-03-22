import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="moodtracker",
    user="ethneystewart"
)

cursor = conn.cursor()