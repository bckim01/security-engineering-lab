import os

import psycopg
from flask import Flask

app = Flask(__name__)


@app.get("/")
def home():
    return {
        "message": "Security Engineering Lab is running",
        "status": "healthy",
    }


@app.get("/db-check")
def database_check():
    try:
        with psycopg.connect(
            host=os.environ["DB_HOST"],
            port=os.environ.get("DB_PORT", "5432"),
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            connect_timeout=3,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_database(), current_user;")
                database_name, database_user = cursor.fetchone()

        return {
            "status": "connected",
            "database": database_name,
            "user": database_user,
        }

    except Exception:
        app.logger.exception("Database connection failed")
        return {
            "status": "error",
            "message": "Unable to connect to PostgreSQL",
        }, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
