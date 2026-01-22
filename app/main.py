from fastapi import FastAPI
from app.api.v1.user_controller import router as user_router

my_app = FastAPI()

my_app.include_router(user_router)

@my_app.get("/")
def root():
    return {"status": "ok"}