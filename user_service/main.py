import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

app = FastAPI(
    redirect_slashes=False,
    title="User Service API",
    description="API for managing users",
    version="0.1.0",
    docs_url='/users/docs',
    redoc_url='/users/redoc',
    openapi_url='/users/openapi.json'
)


# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        port=os.getenv('POSTGRES_PORT')  # Include the port from environment
    )
    return conn

# Pydantic model for the User
class User(BaseModel):
    id: int
    username: str
    email: str

# Endpoint to get all users
@app.get("/users")
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, username, email FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

# Endpoint to add a user
@app.post("/users")
def add_user(user: User):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO users (id, username, email) VALUES (%s, %s, %s)',
        (user.id, user.username, user.email)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "User added successfully"}

# Endpoint to get user details by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, username, email FROM users WHERE id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user[0],
        "username": user[1],
        "email": user[2]
    }
