import logging
import os

from cadquery import Assembly
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from core.deps import get_cad_processor
from processor import CADProcessor
from shared.models.base import CADConfiguration

api_router = APIRouter()

logger = logging.getLogger(__name__)


class GenerateRequest(BaseModel):
    config: CADConfiguration = Field(default_factory=CADConfiguration)


tmp_path = "C:\\Users\\Archie\\PycharmProjects\\think-cad-main\\web\\public"


@api_router.post("/generate")
async def generate(
    request: GenerateRequest, model: CADProcessor = Depends(get_cad_processor)
):
    wp = await model.process_configuration(request.config)
    assy = Assembly()
    assy.add(wp, name="main_workplane")
    assy.export(os.path.join(tmp_path, "output.glb"))

    return {
        "status": "success",
        "message": "CAD model generated successfully",
        "file_path": "output.glb",
    }
