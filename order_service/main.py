import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

app = FastAPI(
    redirect_slashes=False,
    title="Order Service API",
    description="API for managing orders",
    version="0.1.0",
    docs_url='/orders/docs',
    redoc_url='/orders/redoc',
    openapi_url='/orders/openapi.json'
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

# Pydantic model for the Order
class Order(BaseModel):
    id: int
    product_id: int
    user_id: int
    quantity: int

# External service URLs
PRODUCT_SERVICE_URL = "http://product-service:8001/products"
USER_SERVICE_URL = "http://user-service:8002/users"

# Function to fetch product details
async def get_product(product_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/{product_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Product not found")
        return response.json()

# Function to fetch user details
async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}/{user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")
        return response.json()

# Endpoint to get all orders
@app.get("/orders")
def get_orders():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, product_id, user_id, quantity FROM orders')
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return orders

# Endpoint to add a new order
@app.post("/orders")
async def add_order(order: Order):
    # Fetch product and user details before placing the order
    product = await get_product(order.product_id)
    user = await get_user(order.user_id)

    # Assuming product and user details are fetched successfully
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO orders (id, product_id, user_id, quantity) VALUES (%s, %s, %s, %s)',
        (order.id, order.product_id, order.user_id, order.quantity)
    )
    conn.commit()
    cur.close()
    conn.close()

    return {
        "message": "Order placed successfully",
        "order": order,
        "product": product,
        "user": user
    }