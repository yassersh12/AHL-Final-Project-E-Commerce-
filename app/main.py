from fastapi import FastAPI
from app.models import Product
from app.api.routes.product import router as product_router
from app.api.routes.user import router as user_router

app = FastAPI()
app.include_router(product_router)
app.include_router(user_router)


@app.get("/hello")
def read_helo():
    return {"message": "Hello, World!"}
