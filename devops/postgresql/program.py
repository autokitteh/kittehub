"""PostgreSQL connection example for AutoKitteh."""

import os

import autokitteh
import psycopg2


DSN = os.getenv("DSN")


# Required: database operations only work in activities (for workflow reliability).
@autokitteh.activity
def on_trigger(_):
    conn = psycopg2.connect(DSN)

    try:
        with conn.cursor() as cur:
            # Your database operations here.
            cur.execute("SELECT * FROM users")
            results = cur.fetchall()
            print(results)
    finally:
        conn.close()
