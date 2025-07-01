from pydantic import BaseModel, Field


class OrchestratorRequest(BaseModel):
    """Request model for the orchestrator service."""

    prompt: str = Field(description="Prompt to be processed")


class NERRequest(BaseModel):
    prompt: str = Field(..., description="Prompt text")
