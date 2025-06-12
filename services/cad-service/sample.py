import asyncio
import logging

from cadquery import Assembly
from cadquery.vis import show

from processor import CADProcessor
from shared.models.base import (
    CADConfiguration,
    BoxParameters, Shape,
)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def main():
    processor = CADProcessor()

    config = CADConfiguration(
        metadata={"name": "Test", "units": "mm"},
        shapes=[
            Shape(
                type="box",
                parameters=BoxParameters(
                    type="box",
                    centered=True,
                    length=10000.0,
                    width=10000.0,
                    height=10000.0,
                ),
                rotation=[0, 0, 0],
                position=[0, 0, 0],
            )
        ],
    )

    result = await processor.process_configuration(config)
    assy = Assembly()
    assy.add(result, name="main_workplane")
    show(assy)


if __name__ == "__main__":
    asyncio.run(main())
