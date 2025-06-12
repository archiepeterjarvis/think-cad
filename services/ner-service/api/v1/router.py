import logging

import httpx
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from core.deps import get_ner_model
from models.spacy_ner import SpacyNERModel
from utils import entities_to_engine

api_router = APIRouter()

logger = logging.getLogger(__name__)


class NERRequest(BaseModel):
    prompt: str = Field(..., description="Prompt text")


@api_router.post("/extract")
async def extract_entities(
        request: NERRequest, model: SpacyNERModel = Depends(get_ner_model)
):
    """Extract named entities from the provided prompt."""
    entities = model.predict(request.prompt)

    if entities:
        engine_config = entities_to_engine.convert_entities_to_engine_configuration(
            entities
        )

        async with httpx.AsyncClient() as client:
            config_dict = engine_config.model_dump()

            response = await client.post(
                "http://localhost:8001/api/v1/generate",
                json={
                    "config": config_dict
                },
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                return response.json()
            else:
                # Log the error for debugging
                print(
                    f"Error from generation service: {response.status_code} - {response.text}"
                )
                return {
                    "error": "Generation service error",
                    "status_code": response.status_code,
                    "entities": entities,
                }

    return {"entities": entities}
