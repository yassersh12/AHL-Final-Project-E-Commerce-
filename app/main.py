from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.main import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)


@app.get("/hello")
def read_hello():
    return {"message": "Hello, World!"}
