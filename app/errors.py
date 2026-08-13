from fastapi.responses import JSONResponse

from app.schemas.errors import ErrorDetail, ErrorResponse


def upstream_error(
    status_code: int,
    message: str,
    type: str,
    code: str | None,
    param: str | None = None,
) -> JSONResponse:
    body = ErrorResponse(
        error=ErrorDetail(message=message, type=type, param=param, code=code)
    )
    return JSONResponse(status_code=status_code, content=body.model_dump())
