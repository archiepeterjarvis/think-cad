from typing import Optional

from pydantic import BaseModel, Field


class Entity(BaseModel):
    start: int = Field(..., description="Start index of the entity in the text")
    end: int = Field(..., description="End index of the entity in the text")
    label: str = Field(..., description="Label of the entity")
    text: str = Field(..., description="Text of the entity")


class Object(BaseModel):
    type: Optional[str] = Field(..., description="Type of the object")
    modifiers: list[str] = Field(
        default_factory=list, description="List of modifiers for the object"
    )
    parameters: dict = Field(
        default_factory=dict, description="Parameters associated with the object"
    )


class CleanedRequest(BaseModel):
    action: str = Field(..., description="Action verb extracted from the prompt")
    object: Object = Field(
        default_factory=Object, description="Object extracted from the prompt"
    )
