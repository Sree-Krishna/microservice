import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

app = FastAPI(
    redirect_slashes=False,
    title="Product Service API",
    description="API for managing products",
    version="0.1.0",
    docs_url='/products/docs',              # Custom URL for docs
    redoc_url='/products/redoc',            # Custom URL for ReDoc
    openapi_url='/products/openapi.json'    # Custom URL for OpenAPI spec
)

# PostgreSQL connection details from environment variables
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

# Create a PostgreSQL connection
def get_db_connection():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT
    )
    return conn

# Pydantic model for product
class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str

# Endpoint to get all products
@app.get("/products")
def get_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, price, description FROM products')
    products = cur.fetchall()
    cur.close()
    conn.close()
    return products

# Endpoint to add a new product
@app.post("/products")
def add_product(product: Product):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO products (id, name, price, description) VALUES (%s, %s, %s, %s)',
        (product.id, product.name, product.price, product.description)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Product added successfully, working"}

# Endpoint to get product details by ID
@app.get("/products/{product_id}")
def get_product(product_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, price, description FROM products WHERE id = %s', (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "id": product[0],
        "name": product[1],
        "price": product[2],
        "description": product[3]
    }
