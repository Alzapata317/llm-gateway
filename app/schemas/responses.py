from typing import Literal

from ._base import WireModel
from .tools import ChatCompletionMessageToolCall


class UrlCitation(WireModel):
    end_index: int
    start_index: int
    title: str
    url: str  # format says uri


class Annotation(WireModel):
    type: Literal["url_citation"]
    url_citation: UrlCitation


class ChatCompletionMessage(WireModel):
    content: str | None = None
    refusal: str | None = None
    role: Literal["assistant"]
    annotations: list[Annotation] | None = None
    tool_calls: list[ChatCompletionMessageToolCall] | None = None


class Choice(WireModel):
    finish_reason: Literal[
        "stop", "length", "tool_calls", "content_filter", "function_call"
    ]
    index: int
    message: ChatCompletionMessage


class CompletionTokenDetails(WireModel):
    accepted_prediction_tokens: int | None = None
    reasoning_tokens: int | None = None
    rejected_prediction_tokens: int | None = None


class PromptTokensDetails(WireModel):
    cache_write_tokens: int | None = None
    cached_tokens: int | None = None


class CompletionUsage(WireModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    completion_tokens_details: CompletionTokenDetails | None = None
    prompt_tokens_details: PromptTokensDetails | None = None


class ChatCompletion(WireModel):
    id: str
    choices: list[Choice]
    created: int
    model: str
    object: Literal["chat.completion"]
    usage: CompletionUsage | None = None
