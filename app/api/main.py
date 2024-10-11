from fastapi import FastAPI
from app.api.main import api_router
from app.db.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)


@app.get("/hello")
def read_helo():
    return {"message": "Hello, World!"}
