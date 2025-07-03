"""PostgreSQL connection example for AutoKitteh."""

import os

import autokitteh
import psycopg2


HOST = os.getenv("POSTGRES_HOST")
PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DATABASE = os.getenv("POSTGRES_DATABASE")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")


def open_connection():
    return psycopg2.connect(
        host=HOST, port=PORT, database=DATABASE, user=USER, password=PASSWORD
    )


# Required: database operations only work in activities (for workflow reliability).
@autokitteh.activity
def on_trigger(event):
    conn = open_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users")
            results = cur.fetchall()
            print(results)
    finally:
        conn.close()
