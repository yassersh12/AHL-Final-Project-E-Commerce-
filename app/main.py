from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.main import api_router
from app.api.exceptions.global_exceptions import global_exception_handler

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_exception_handler(Exception, global_exception_handler)


app.include_router(api_router, prefix="/api/v1")


@app.get("/hello")
def read_hello():
    return {"message": "Hello, World!"}
