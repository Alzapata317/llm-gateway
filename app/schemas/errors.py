from ._base import WireModel


class ErrorDetail(WireModel):
    message: str
    type: str
    param: str | None = None
    code: str | None = None


class ErrorResponse(WireModel):
    error: ErrorDetail
