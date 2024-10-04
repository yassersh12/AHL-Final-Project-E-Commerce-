from fastapi import FastAPI
from app.models import Product
from app.api.routes.product import router as product_router

app = FastAPI()
app.include_router(product_router)


@app.get("/hello")
def read_helo():
    return {"message": "Hello, World!"}
