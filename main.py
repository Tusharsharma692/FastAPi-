from fastapi import FastAPI,Request,HTTPException
import sqlite3
from pydantic import BaseModel

app=FastAPI()

con = sqlite3.connect("DEMO.db",check_same_thread=False)
cursor=con.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS USERS(
               ID INTEGER PRIMARY KEY,
               NAME TEXT,
               JOB TEXT)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS TODOS(
               ID INTEGER PRIMARY KEY,
               ACTIVITY TEXT)
""")

con.commit()

class User(BaseModel):
    ID:int
    NAME:str
    JOB:str


class Todo(BaseModel):
    ID:int
    ACTIVITY:str


@app.middleware("http")
async def demo(request:Request,call_next):

    print("Request Received")
    print(f"Path : {request.url.path}")
    response = await call_next(request)
    print("Response Sent")

    return response


@app.post("/users")
def create_user(user: User):

    try:
        cursor.execute(
            "INSERT INTO USERS VALUES (?,?,?)",
            (user.ID, user.NAME, user.JOB)
        )

        con.commit()

        return {
            "message": "User created successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.get("/users/{user_id}")
def get_user(user_id: int):

    cursor.execute(
        "SELECT * FROM USERS WHERE ID=?",
        (user_id,)
    )

    user = cursor.fetchone()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "ID": user[0],
        "NAME": user[1],
        "JOB": user[2]
    }

@app.get("/users")
def get_all_users():

    cursor.execute("SELECT * FROM USERS")

    users = cursor.fetchall()

    return [
        {
            "ID": user[0],
            "NAME": user[1],
            "JOB": user[2]
        }
        for user in users
    ]

# Todo apis
@app.post("/todos")
def create_todo(todo: Todo):

    try:
        cursor.execute(
            "INSERT INTO TODOS VALUES (?,?)",
            (todo.ID, todo.ACTIVITY)
        )

        con.commit()

        return {
            "message": "Todo created successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):

    cursor.execute(
        "SELECT * FROM TODOS WHERE ID=?",
        (todo_id,)
    )

    todo = cursor.fetchone()

    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return {
        "ID": todo[0],
        "ACTIVITY": todo[1]
    }

@app.get("/todos")
def get_all_todos():

    cursor.execute("SELECT * FROM TODOS")

    todos = cursor.fetchall()

    return [
        {
            "ID": todo[0],
            "ACTIVITY": todo[1]
        }
        for todo in todos
    ]
