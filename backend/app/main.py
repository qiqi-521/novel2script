"""FastAPI application entrypoint."""

from fastapi import FastAPI

from backend.app.api.routes import router

app = FastAPI(
    title="novel2script backend",
    version="0.1.0",
    description="Backend service for structured novel-to-script generation.",
)

app.include_router(router)
