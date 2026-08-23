from contextlib import asynccontextmanager
import asyncio
import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host = os.getenv("MYSQL_HOST", "mysql"),
        user = os.getenv("MYSQL_USER", "appuser"),
        password = os.getenv("MYSQL_PASSWORD", "apppassword"),
        database = os.getenv("MYSQL_DATABASE", "tasksdb"),
    )

@asynccontextmanager
async def lifespan(app):
    conn = None

    for attempt in range(10):
        try:
            conn = get_connection()
            break
        except mysql.connector.Error as e:
            print(f"MySQL connection attempt {attempt + 1}/10 failed: {e}")
            if attempt == 9:
                raise
            await asyncio.sleep(2)
            
    try:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255)
            )
        """)

        conn.commit()
        cur.close()

        # Startup finished
        yield
    finally:
        conn.close()
