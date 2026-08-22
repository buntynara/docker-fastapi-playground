from app.core.database import get_connection
from app.schemas.task import TaskCreate

def get_tasks():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM tasks ORDER BY id")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def create_task(task: TaskCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks(title) VALUES(%s)", (task.title,))
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return {"id": new_id, "title": task.title}