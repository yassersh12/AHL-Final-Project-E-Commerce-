from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.routes import user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the User Management API"}


@app.get("/hello")
def read_helo():
    return {"message": "Hello, World!"}
