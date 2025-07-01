from typing import Optional

from pydantic import BaseModel, Field

from shared.models.misc import Entity


class NERResponse(BaseModel):
    error: Optional[str] = Field(None, description="Error message if any")
    entities: Optional[list[Entity]] = Field(
        default_factory=list, description="List of extracted entities"
    )

