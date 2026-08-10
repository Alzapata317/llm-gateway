from typing import Annotated, Literal

from pydantic import Field

from ._base import WireModel
from .content import (
    ArrayOfContentParts,
    ChatCompletionContentPart,
    ChatCompletionContentPartText,
)
from .tools import ChatCompletionMessageToolCall


class ChatCompletionDeveloperMessageParam(WireModel):
    content: str | list[ChatCompletionContentPartText]
    role: Literal["developer"]
    name: str | None = None


class ChatCompletionSystemMessageParam(WireModel):
    content: str | list[ChatCompletionContentPartText]
    role: Literal["system"]
    name: str | None = None


class ChatCompletionUserMessageParam(WireModel):
    content: str | list[ChatCompletionContentPart]
    role: Literal["user"]
    name: str | None = None


class ChatCompletionAssistantMessageParam(WireModel):
    role: Literal["assistant"]
    content: str | list[ArrayOfContentParts] | None = None
    name: str | None = None
    refusal: str | None = None
    tool_calls: list[ChatCompletionMessageToolCall] | None = None


class ChatCompletionToolMessageParam(WireModel):
    content: str | list[ChatCompletionContentPartText]
    role: Literal["tool"]
    tool_call_id: str


class ChatCompletionFunctionMessageParam(WireModel):
    content: str | None = None
    name: str
    role: Literal["function"]


ChatCompletionMessageParam = Annotated[
    ChatCompletionDeveloperMessageParam
    | ChatCompletionSystemMessageParam
    | ChatCompletionUserMessageParam
    | ChatCompletionAssistantMessageParam
    | ChatCompletionToolMessageParam
    | ChatCompletionFunctionMessageParam,
    Field(discriminator="role"),
]


class ChatCompletionRequest(WireModel):
    model: str
    messages: list[ChatCompletionMessageParam]
    stream: bool = False
    reasoning_effort: (
        Literal["none", "minimal", "low", "medium", "high", "xhigh", "max"] | None
    ) = None
