from contextlib import asynccontextmanager
import asyncio
import mysql.connector
from app.core.config import get_settings

settings = get_settings()
app_ready = False

def get_connection():
    return mysql.connector.connect(
        host = settings.MYSQL_HOST,
        port = settings.MYSQL_PORT,
        user = settings.MYSQL_USER,
        password = settings.MYSQL_PASSWORD,
        database = settings.MYSQL_DATABASE
    )

@asynccontextmanager
async def lifespan(app):
    global app_ready
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

        app_ready = True

        # Startup finished
        yield

        # Shutdown logic
        app_ready = False
    finally:
        conn.close()
