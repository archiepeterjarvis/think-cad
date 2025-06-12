import logging

from cadquery import cq

from processor.gears import get_gear_handlers
from processor.interfaces import ShapeHandler, GearHandler, OperationHandler, Exporter
from processor.shapes import get_shape_handlers
from shared.models.base import CADConfiguration

logger = logging.getLogger(__name__)


class CADProcessor:
    """Main processor that coordinates all CAD operations"""

    def __init__(self, cache: bool = True):
        self.shape_handlers: dict[str, ShapeHandler] = {}
        self.gear_handlers: dict[str, GearHandler] = {}
        self.operation_handlers: dict[str, OperationHandler] = {}
        self.exporters: dict[str, Exporter] = {}

        self._register_handlers()

    def _register_handlers(self):
        """Register all available handlers"""
        for handler_class in get_shape_handlers():
            handler = handler_class()
            for shape_type in handler.supported_types:
                self.shape_handlers[shape_type] = handler
                logger.debug(
                    f"Registered shape: {shape_type} (handler: {handler_class.__name__})"
                )

        for handler_class in get_gear_handlers():
            handler = handler_class()
            for gear_type in handler.supported_types:
                self.gear_handlers[gear_type] = handler
                logger.debug(
                    f"Registered gear: {gear_type} (handler: {handler_class.__name__})"
                )

    async def process_configuration(self, config: CADConfiguration) -> cq.Workplane:
        """Main processing entry point"""

        result = await self._process_components(config)

        logger.info("CAD configuration processing complete")
        return result

    async def _process_components(self, config: CADConfiguration) -> cq.Workplane:
        """Process all components in the configuration"""
        components = {}
        result = None

        if config.shapes:
            for i, shape in enumerate(config.shapes):
                shape_id = shape.id or f"shape_{i}"
                logger.debug(f"Processing shape: {shape_id} (type: {shape.type})")

                handler = self.shape_handlers.get(shape.type)
                if not handler:
                    raise ValueError(f"No handler for shape type {shape.type}")

                shape_obj = await handler.create(
                    shape.parameters, shape.position, shape.rotation
                )
                components[shape_id] = shape_obj

                result = shape_obj if result is None else result.union(shape_obj)

        if config.gears:
            for i, gear in enumerate(config.gears):
                gear_id = gear.id or f"gear_{i}"
                logger.debug(f"Processing gear: {gear_id} (type: {gear.type})")

                handler = self.gear_handlers.get(gear.type)
                if not handler:
                    raise ValueError(f"No handler for gear type {gear.type}")

                gear_obj = await handler.create(
                    gear.parameters, gear.position, gear.rotation
                )
                components[gear_id] = gear_obj

                result = gear_obj if result is None else result.union(gear_obj)

        if config.operations:
            for operation in config.operations:
                logger.debug(f"Processing operation (type: {operation.type})")

                handler = self.operation_handlers.get(operation.type)
                if not handler:
                    raise ValueError(f"No handler for operation type {operation.type}")

                result = await handler.apply(result, operation, components)

        return result or cq.Workplane("XY")
