from enum import Enum
from typing import Optional, List, Tuple, Literal, Union

from pydantic import BaseModel, Field

from shared.models.features import FeatureUnion


class Units(str, Enum):
    MM = "mm"
    CM = "cm"
    M = "m"
    IN = "in"
    FT = "ft"


class Plane(str, Enum):
    XY = "XY"
    XZ = "XZ"
    YZ = "YZ"


class ExportFormat(str, Enum):
    STEP = "step"
    STL = "stl"
    OBJ = "obj"
    PLY = "ply"
    AMF = "amf"
    THREE_MF = "3mf"


class Metadata(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    units: Units = Units.MM


class Workplane(BaseModel):
    plane: Plane = Plane.XY
    offset: float = 0
    origin: Optional[List[float]] = Field(None, min_items=2, max_items=3)


class BoxParameters(BaseModel):
    type: Literal["box"] = "box"
    length: float = Field(..., gt=0)
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    centered: bool = False
    features: Optional[List[FeatureUnion]] = []


class CylinderParameters(BaseModel):
    type: Literal["cylinder"] = "cylinder"
    radius: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    centered: bool = False
    angle: float = Field(..., ge=0, le=360)
    features: Optional[List[FeatureUnion]] = []


class SphereParameters(BaseModel):
    type: Literal["sphere"] = "sphere"
    radius: float = Field(..., gt=0)
    angle1: float = Field(-90, ge=-90, le=90)
    angle2: float = Field(90, ge=-90, le=90)
    angle3: float = Field(360, ge=0, le=360)
    centered: bool = False
    features: Optional[List[FeatureUnion]] = []


class ConeParameters(BaseModel):
    type: Literal["cone"] = "cone"
    radius1: float = Field(..., ge=0)
    radius2: float = Field(..., ge=0)
    height: float = Field(..., gt=0)
    centered: bool = True
    angle: float = Field(360, ge=0, le=360)
    features: Optional[List[FeatureUnion]] = []


class TorusParameters(BaseModel):
    type: Literal["torus"] = "torus"
    major_radius: float = Field(..., gt=0)
    minor_radius: float = Field(..., gt=0)
    angle1: float = Field(0, ge=0, le=360)
    angle2: float = Field(360, ge=0, le=360)
    angle3: float = Field(360, ge=0, le=360)
    features: Optional[List[FeatureUnion]] = []


class WedgeParameters(BaseModel):
    type: Literal["wedge"] = "wedge"
    dx: float = Field(..., gt=0)
    dy: float = Field(..., gt=0)
    dz: float = Field(..., gt=0)
    zmin: float = 0
    xmin: float = 0
    xmax: float = 0
    zmax: float = 0
    features: Optional[List[FeatureUnion]] = []


class ExtrudeParameters(BaseModel):
    type: Literal["extrude"] = "extrude"
    profile: List[Tuple[float, float]]
    distance: float
    both: bool = False
    taper: float = 0


class TextParameters(BaseModel):
    type: Literal["text"] = "text"
    text: str
    fontsize: float = Field(12, gt=0)
    distance: float = Field(..., gt=0)
    font: str = "Arial"
    fontPath: Optional[str] = None
    kind: Literal["regular", "bold", "italic"] = "regular"
    halign: Literal["center", "left", "right"] = "center"
    valign: Literal["center", "bottom", "top"] = "center"


class Shape(BaseModel):
    id: Optional[str] = None
    type: Literal[
        "box",
        "cylinder",
        "sphere",
        "cone",
        "torus",
        "wedge",
        "extrude",
        "revolve",
        "loft",
        "sweep",
        "text",
    ]
    parameters: Union[
        BoxParameters,
        CylinderParameters,
        SphereParameters,
        ConeParameters,
        TorusParameters,
        WedgeParameters,
        ExtrudeParameters,
        TextParameters,
    ] = Field(..., discriminator="type")
    position: List[float] = Field([0, 0, 0], min_items=3, max_items=3)
    rotation: List[float] = Field([0, 0, 0], min_items=3, max_items=3)


class SpurGearParameters(BaseModel):
    type: Literal["spur_gear"] = "spur_gear"
    module: float = Field(..., gt=0)
    teeth: int = Field(..., ge=3)
    width: float = Field(..., gt=0)
    bore: float = Field(0, ge=0)
    pressure_angle: float = Field(20, ge=0, le=45)
    clearance: float = Field(0, ge=0)
    backlash: float = Field(0, ge=0)
    profile_shift: float = 0
    hub_diameter: Optional[float] = Field(None, gt=0)
    hub_length: Optional[float] = Field(None, gt=0)
    rim_width: Optional[float] = Field(None, gt=0)


class BevelGearParameters(BaseModel):
    type: Literal["bevel_gear"] = "bevel_gear"
    module: float = Field(..., gt=0)
    teeth: int = Field(..., ge=3)
    cone_angle: float = Field(..., ge=0, le=90)
    pressure_angle: Optional[float] = Field(0, ge=0, le=45)
    helix_angle: Optional[float] = Field(0, ge=0, le=180)
    bore: float = Field(0, ge=0)
    clearance: Optional[float] = Field(0, ge=0)
    backlash: Optional[float] = Field(0, ge=0)
    face_width: Optional[float] = Field(0, gt=0)


# TODO: Add other gear types


class Gear(BaseModel):
    id: Optional[str] = None
    type: Literal["spur", "bevel"]
    parameters: Union[SpurGearParameters, BevelGearParameters] = Field(
        ..., discriminator="type"
    )
    position: List[float] = Field([0, 0, 0], min_items=3, max_items=3)
    rotation: List[float] = Field([0, 0, 0], min_items=3, max_items=3)


class FilletParameters(BaseModel):
    type: Literal["fillet"] = "fillet"
    radius: float = Field(..., gt=0)
    edges: Optional[List[str]] = None


class ChamferParameters(BaseModel):
    type: Literal["chamfer"] = "chamfer"
    length: float = Field(..., gt=0)
    edges: Optional[List[str]] = None


class ShellParameters(BaseModel):
    type: Literal["shell"] = "shell"
    thickness: float = Field(..., gt=0)
    faces: Optional[List[str]] = None


class ArrayParameters(BaseModel):
    type: Literal["array"] = "array"
    count: int = Field(..., gt=1)
    spacing: List[float] = Field(..., min_items=3, max_items=3)


class PatternParameters(BaseModel):
    type: Literal["pattern"] = "pattern"
    pattern_type: Literal["linear", "circular", "rectangular"]
    count: int = Field(..., ge=1)
    spacing: Optional[float] = Field(None, gt=0)
    angle: float = 0
    center: Optional[List[float]] = Field(None, min_items=3, max_items=3)


class BooleanParameters(BaseModel):
    type: Literal["boolean"] = "boolean"
    tool: str


class Operation(BaseModel):
    type: Literal[
        "union",
        "cut",
        "intersect",
        "fillet",
        "chamfer",
        "shell",
        "mirror",
        "array",
        "pattern",
    ]
    targets: List[str]
    parameters: Optional[
        Union[
            BooleanParameters,
            FilletParameters,
            ChamferParameters,
            ShellParameters,
            ArrayParameters,
            PatternParameters,
        ]
    ] = Field(None, discriminator="type")


class LineParameters(BaseModel):
    type: Literal["line"] = "line"
    start: Tuple[float, float]
    end: Tuple[float, float]


class ArcParameters(BaseModel):
    type: Literal["arc"] = "arc"
    center: Tuple[float, float]
    radius: float = Field(..., gt=0)
    start_angle: float
    end_angle: float


class CircleParameters(BaseModel):
    type: Literal["circle"] = "circle"
    center: Tuple[float, float]
    radius: float = Field(..., gt=0)


class RectangleParameters(BaseModel):
    type: Literal["rectangle"] = "rectangle"
    corner1: Tuple[float, float]
    corner2: Tuple[float, float]


class PolygonParameters(BaseModel):
    type: Literal["polygon"] = "polygon"
    points: List[Tuple[float, float]] = Field(..., min_items=3)


class SketchElement(BaseModel):
    type: Literal["line", "arc", "circle", "rectangle", "polygon", "spline", "bezier"]
    parameters: Union[
        LineParameters,
        ArcParameters,
        CircleParameters,
        RectangleParameters,
        PolygonParameters,
    ] = Field(..., discriminator="type")


class Constraint(BaseModel):
    type: Literal[
        "coincident",
        "parallel",
        "perpendicular",
        "tangent",
        "horizontal",
        "vertical",
        "equal",
        "distance",
        "angle",
    ]
    elements: List[str]
    value: Optional[float] = None


class Sketch(BaseModel):
    elements: Optional[List[SketchElement]] = None
    constraints: Optional[List[Constraint]] = None


class Export(BaseModel):
    format: ExportFormat = ExportFormat.STEP
    filename: Optional[str] = None
    precision: float = Field(0.1, gt=0)
    angular_tolerance: float = Field(0.1, gt=0)
    binary: bool = True


class CADConfiguration(BaseModel):
    metadata: Optional[Metadata] = None
    workplane: Optional[Workplane] = None
    shapes: List[Shape] = []
    gears: Optional[List[Gear]] = None
    operations: Optional[List[Operation]] = None
    sketch: Optional[Sketch] = None
    export: Optional[Export] = None

    class Config:
        extra = "allow"
        use_enum_values = True
