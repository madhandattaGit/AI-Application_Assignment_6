from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class TextInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    text: Annotated[
        str,
        Field(
            ...,
            min_length=1,
            max_length=5000,
            strict=True,
            description="Text to summarize.",
        ),
    ]


class SummaryResponse(BaseModel):
    summary: str


class ErrorResponse(BaseModel):
    error: str
    details: list[str] = []
