import asyncio
import time
import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schemas.errors import ErrorDetail, ErrorResponse
from app.schemas.requests import ChatCompletionRequest
from app.schemas.responses import (
    ChatCompletion,
    ChatCompletionMessage,
    Choice,
    CompletionUsage,
)

router = APIRouter()

SLOW_DELAY_S = 60.0


def _last_user_text(request: ChatCompletionRequest) -> str:
    for message in reversed(request.messages):
        if message.role != "user":
            continue
        if isinstance(message.content, str):
            return message.content
        # Content-part array: concatenate the text parts, ignore images/files.
        return " ".join(part.text for part in message.content if part.type == "text")
    return "(no user message)"


def _completion(request: ChatCompletionRequest, content: str) -> ChatCompletion:
    return ChatCompletion(
        id=f"chatcmpl-stub-{uuid.uuid4().hex[:24]}",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(role="assistant", content=content),
            )
        ],
        created=int(time.time()),
        model=request.model,
        object="chat.completion",
        usage=CompletionUsage(
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
        ),
    )


def _error(
    status_code: int, message: str, type_: str, code: str | None
) -> JSONResponse:
    body = ErrorResponse(
        error=ErrorDetail(message=message, type=type_, param=None, code=code)
    )
    return JSONResponse(status_code=status_code, content=body.model_dump())


@router.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    if request.model == "stub-500":
        return _error(
            status_code=500,
            message="The stub upstream failed on purpose.",
            type_="server_error",
            code="stub_injected_failure",
        )

    if request.model == "stub-slow":
        await asyncio.sleep(SLOW_DELAY_S)

    return _completion(request, f"stub echo: {_last_user_text(request)}")
