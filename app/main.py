import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.config import settings

from .routers import chat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    resolved = settings.model_dump()
    resolved["openai_api_key"] = "***"
    logger.info("resolved settings: %s", resolved)
    async with httpx.AsyncClient(timeout=settings.request_timeout_s) as client:
        app.state.http_client = client
        yield


app = FastAPI(title="LLM Gateway", lifespan=lifespan)
app.include_router(chat.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
