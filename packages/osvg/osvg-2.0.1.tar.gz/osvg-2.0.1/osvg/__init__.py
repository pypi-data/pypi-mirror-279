"""
Object-oriented SVG Drawing Tool
"""

from .float import (
    Float,
    Sum,
    Sub,
    Mul,
    Div,
    FloorDiv,
    Mod,
    Pow,
)
from .float_math import (
    Cos,
    Sin,
    Cot,
    Tan,
    FunctFloat,
    Min,
    LowestAbs,
    Max,
)
from .elements.circle import Circle
from .elements.elementbase import (
    Height,
    Width,
)
from .elements.ellipse import Ellipse
from .elements.group import Group
from .elements.line import Line
from .elements.line_marker import (
    CircleMarker,
    ArrowMarker,
    LightArrowMarker,
    SkinnyArrowMarker,
)
from .elements.text import Text, TextSpan
from .elements.path import (
    Path,
    PathA,
    PathC,
    Pathc,
    PathH,
    Pathh,
    PathL,
    Pathl,
    PathM,
    Pathm,
    PathQ,
    Pathq,
    PathS,
    Paths,
    PathT,
    Patht,
    PathV,
    Pathv,
    PathZ,
)
from .elements.polyline import Polyline
from .elements.rectangle import Rectangle, SCRectangle
from .elements.svg import SVG, ViewBox
from .positions import (
    Position,
    XShiftedPosition,
    YShiftedPosition,
    PolarShiftedPosition,
    RotatedPosition,
    Distance,
    AngleDegree,
)
from .style import (
    FillColor,
    FillOpacity,
    StrokeDashArray,
    StrokeColor,
    StrokeLineCap,
    StrokeLineJoin,
    StrokeOpacity,
    StrokeWidth,
    Style,
)

__version__ = "2.0.1"
version_info = (2, 0, 1)
