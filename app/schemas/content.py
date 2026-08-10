from typing import Annotated, Literal

from pydantic import Field

from ._base import WireModel


class ChatCompletionContentPartText(WireModel):
    text: str
    type: Literal["text"]


class ImageUrl(WireModel):
    url: str
    detail: Literal["auto", "low", "high"] | None = None


class ChatCompletionContentPartImage(WireModel):
    image_url: ImageUrl
    type: Literal["image_url"]


class File(WireModel):
    file_data: str | None = None
    file_id: str | None = None
    filename: str | None = None


class FileContentPart(WireModel):
    file: File
    type: Literal["file"]


ChatCompletionContentPart = Annotated[
    ChatCompletionContentPartText | ChatCompletionContentPartImage | FileContentPart,
    Field(discriminator="type"),
]


class ChatCompletionContentPartRefusal(WireModel):
    refusal: str
    type: Literal["refusal"]


ArrayOfContentParts = Annotated[
    ChatCompletionContentPartText | ChatCompletionContentPartRefusal,
    Field(discriminator="type"),
]
