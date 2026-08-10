from typing import Annotated, Literal

from pydantic import Field

from ._base import WireModel


class Custom(WireModel):
    input: str
    name: str


class ChatCompletionMessageCustomToolCall(WireModel):
    id: str
    custom: Custom
    type: Literal["custom"]


class Function(WireModel):
    arguments: str
    name: str


class ChatCompletionMessageFunctionToolCall(WireModel):
    id: str
    function: Function
    type: Literal["function"]


ChatCompletionMessageToolCall = Annotated[
    ChatCompletionMessageFunctionToolCall | ChatCompletionMessageCustomToolCall,
    Field(discriminator="type"),
]
