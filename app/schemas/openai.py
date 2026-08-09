from typing import Literal

from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    role: Literal["user", "assistant", "system", "tool", "developer"]
    content: str
    name: str | None = None


class ChatCompletionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    model: str
    messages: list[Message]
    stream: bool = False
    reasoning_effort: (
        Literal["none", "minimal", "low", "medium", "high", "xhigh", "max"] | None
    ) = None
