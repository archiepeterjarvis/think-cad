from shared.models.base import CADConfiguration, Shape, BoxParameters

SHAPE_MAPPING = {
    "cube": "box",
}


def convert_entities_to_engine_configuration(
        entities: list[dict],
) -> CADConfiguration:
    """Convert entities to CADConfiguration."""

    config = CADConfiguration(shapes=[])

    for entity in entities:
        if entity["label"].lower() == "shape":
            shape = entity["text"].lower()

        if entity["label"].lower() == "dimension":
            dimension = float(entity["text"])

        if entity["label"].lower() == "unit":
            unit = entity["text"].lower()

    config.shapes.append(
        Shape(
            type=SHAPE_MAPPING[shape],
            parameters=BoxParameters(
                type="box",
                width=dimension,
                height=dimension,
                length=dimension,
                centered=True,
            ),
            position=[0, 0, 0],
            rotation=[0, 0, 0],
        )
    )

    return config
