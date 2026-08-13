import logging

import httpx
from fastapi import APIRouter
from fastapi.responses import Response

from app.config import settings
from app.dependencies import HttpClientDep
from app.errors import upstream_error
from app.schemas.requests import ChatCompletionRequest

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, client: HttpClientDep):
    url = f"{settings.openai_base_url}/chat/completions"
    try:
        response = await client.post(
            url,
            json=request.model_dump(exclude_unset=True),
            headers={
                "Authorization": f"Bearer {settings.openai_api_key.get_secret_value()}"
            },
        )
    except httpx.TimeoutException:
        # The upstream did not answer within settings.request_timeout_s.
        # Nothing came back, so there is no upstream response to relay - the
        # gateway has to generate its own OpenAI-shaped error instead.
        logger.exception(
            "upstream timeout: url=%s model=%s",
            url,
            request.model,
        )
        return upstream_error(
            status_code=504,
            message=(
                f"The upstream provider did not respond within "
                f"{settings.request_timeout_s} seconds."
            ),
            type="upstream_timeout",
            param=None,
            code="upstream_timeout",
        )
    except httpx.ConnectError:
        logger.exception(
            "connection error: url=%s model=%s",
            url,
            request.model,
        )
        return upstream_error(
            status_code=502,
            message="The gateway could not connect to provider",
            type="connect_error",
            param=None,
            code="connect_error",
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type="application/json",
    )
