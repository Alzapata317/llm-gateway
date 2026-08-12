from fastapi import FastAPI

from .routers import chat

app = FastAPI()

app.include_router(chat.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
