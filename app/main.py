from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="BE AI TUTOR")

app.include_router(router)
