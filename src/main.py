from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.controllers import health_controller
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url="/api/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (Controllers)
app.include_router(health_controller.router, tags=["Health"])


@app.get("/")
def root():
    return {"status": "healthy", "version": settings.VERSION}
