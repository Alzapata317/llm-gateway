import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    resolved = settings.model_dump()
    resolved["openai_api_key"] = "***"
    logger.info("resolved settings: %s", resolved)
    yield


app = FastAPI(title="LLM Gateway", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
