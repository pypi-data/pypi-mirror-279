"""
Module to define style classes.
"""

# pylint: disable=too-few-public-methods

from typing import TypedDict
from typing_extensions import Unpack
import osvg.float


def verify_hex_string(hex_value: str) -> bool:
    """
    Verify if given string represents a hexadecimal value
    """
    try:
        int(hex_value, 16)
    except (TypeError, ValueError):
        return False
    return True


def verify_color_value(value):
    """
    Verify if given string is a valid value for a color style attribute
    """
    if (
        value is not None
        and value != "none"
        and (
            not isinstance(value, str)
            or len(value) != 6
            or not verify_hex_string(value)
        )
    ):
        raise TypeError("hex_def must be a string of 6 hex values or 'none'")


class StyleAttribute:
    """
    Base class for all style attribute classes
    """

    key = ""
    default = None
    allowed_value_classes = ()

    def __init__(self, value: any = None) -> None:
        self.value = value

    @property
    def isdefault(self) -> bool:
        """
        Check, if object's value is set to class default.
        """
        return self.value == self.default

    def equals(self, other) -> bool:
        """
        Check, if other's string value is equal to self's string value
        """
        return self.value == other.value

    def copy(self):
        """
        Return an object with the same float value as value
        """
        return self.__class__(value=self.value)

    @property
    def _value_str(self) -> str:
        """
        Get str of value
        """
        return str(self.value)

    def __str__(self) -> str:
        # pylint: disable=singleton-comparison
        return "" if self.value == None else f"{self.key}:{self._value_str}"


class StyleStringAttribute(StyleAttribute):
    """
    Parent class for all string-based style attributes.
    """

    allowed_value_classes = str

    def __init__(self, value: str = None) -> None:
        self._value = None
        super().__init__(value)

    @property
    def value(self):
        """
        Get value
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Set value
        """
        self._verify_value(value)
        self._value = value

    def _verify_value(self, value) -> None:
        """
        Verify value
        """
        if value is not self.default:
            if self.allowed_value_classes and not isinstance(
                value, self.allowed_value_classes
            ):
                raise ValueError(
                    f"Style attribute value must be one of {self.allowed_value_classes}"
                )


class StyleFloatAttribute(StyleAttribute):
    """
    Parent class for all Float based style attributes.
    """

    value = osvg.float.FloatProperty()

    def __init__(self, value: float | osvg.float.Float = None) -> None:
        super().__init__(value=value)


class Color(StyleStringAttribute):
    """
    SVG representation of a color in string of hex values or "none".
    "rrggbb" ->:
        - "rr" 256 bit value for red
        - "gg" 256 bit value for green
        - "bb" 256 bit value for blue
    """

    def __init__(self, value: str = None) -> None:
        super().__init__(value=value)

    def _verify_value(self, value):
        verify_color_value(value)

    @property
    def _value_str(self) -> str:
        return "none" if self.value == "none" else f"#{self.value}"


class Opacity(StyleFloatAttribute):
    """
    SVG representation of a opacity in float 0 <= value <= 1
    with 1 is 100% opacity.
    """

    key = "opacity"


class FillColor(Color):
    """
    SVG Style Attribute "fill"
    """

    key = "fill"


class FillOpacity(Opacity):
    """
    SVG Style Attribute "fill-opacity"
    """

    key = "fill-opacity"


class StrokeColor(Color):
    """
    SVG Style Attribute "stroke"
    """

    key = "stroke"


class StrokeOpacity(Opacity):
    """
    SVG Style Attribute "stroke-opacity"
    """

    key = "stroke-opacity"


class StrokeWidth(StyleFloatAttribute):
    """
    SVG Style Attribute "stroke-width"
    """

    key = "stroke-width"


class StrokeLineCap(StyleStringAttribute):
    """
    SVG Style Attribute "stroke-width"
    """

    key = "stroke-linecap"

    def __init__(self, value: str = None) -> None:
        if value and value not in ["butt", "round", "square"]:
            raise ValueError(f"'{value}' not a valid linecap option")
        super().__init__(value=value)


class StrokeDashArray(osvg.float.FloatList):
    """
    SVG Style Attribute "stroke-width"
    """

    key = "stroke-dasharray"
    name = "values"

    def __str__(self) -> str:
        if not self.values:
            return ""
        return f"{self.key}:{super().__str__()}"


class StrokeLineJoin(StyleStringAttribute):
    """
    SVG Style Attribute "stroke-linejoin"
    """

    key = "stroke-linejoin"

    def __init__(self, value: str = None) -> None:
        if value and value not in [
            "arcs",
            "bevel",
            "miter",
            "miter-clip",
            "round",
        ]:
            raise ValueError(f"'{value}' not a valid linecap option")
        super().__init__(value=value)


class FontFamily(StyleStringAttribute):
    """
    SVG Font Style Attribute "font-family"
    """

    key = "font-family"


class FontSize(StyleFloatAttribute):
    """
    SVG Font Style Attribute "font-size" in pixels
    """

    key = "font-size"

    @property
    def _value_str(self) -> str:
        return f"{str(self.value)}px"


class FontSizeAdjust(StyleFloatAttribute):
    """
    SVG Font Style Attribute "font-size-adjust" in pixels
    """

    key = "font-size-adjust"


class FontStretch(StyleStringAttribute):
    """
    SVG Font Style Attribute "font-stretch"
    """

    key = "font-stretch"


class FontStyle(StyleStringAttribute):
    """
    SVG Font Style Attribute "font-style"
    """

    key = "font-style"
    allowed_values = [
        "normal",
        "italic",
        "oblique",
    ]

    def __init__(self, value: str = None) -> None:
        super().__init__(value)
        if value is not None and value not in self.allowed_values:
            raise ValueError(
                f"font-style value mus be on of {','.join(self.allowed_values)}"
            )


class FontVariant(StyleStringAttribute):
    """
    SVG Font Style Attribute "font-variant"
    """

    key = "font-variant"


class FontWeigth(StyleStringAttribute):
    """
    SVG Font Style Attribute "font-weigth"
    """

    key = "font-weight"
    allowed_values = [
        "normal",
        "bold",
        "bolder",
        "lighter",
    ]

    def __init__(self, value: str = None) -> None:
        super().__init__(value)
        if value is not None and value not in self.allowed_values:
            raise ValueError(
                f"font-weigth value must be on of {','.join(self.allowed_values)}"
            )


class StyleParamTypes(TypedDict):
    """
    Parameter type hint for class Style
    """

    opacity: Opacity | float | int
    fill_color: FillColor | str
    fill_opacity: FillOpacity | float | int
    stroke_color: StrokeColor | str
    stroke_opacity: StrokeOpacity | float | int
    stroke_width: StrokeWidth | float | int
    stroke_linecap: StrokeLineCap | str
    stroke_linejoin: StrokeLineJoin | str
    stroke_dasharray: StrokeDashArray | str
    font_family: FontFamily | str
    font_size: FontSize | float | int
    font_size_adjust: FontSizeAdjust | float | int
    font_stretch: FontStretch | str
    font_style: FontStyle | str
    font_variant: FontVariant | str
    font_weigth: FontWeigth | str
    reference: "Style"


class Style:
    """
    SVG Style representative.
    """

    param_classes = {
        "opacity": Opacity,
        "fill_color": FillColor,
        "fill_opacity": FillOpacity,
        "stroke_color": StrokeColor,
        "stroke_opacity": StrokeOpacity,
        "stroke_width": StrokeWidth,
        "stroke_linecap": StrokeLineCap,
        "stroke_linejoin": StrokeLineJoin,
        "stroke_dasharray": StrokeDashArray,
        "font_family": FontFamily,
        "font_size": FontSize,
        "font_size_adjust": FontSizeAdjust,
        "font_stretch": FontStretch,
        "font_style": FontStyle,
        "font_variant": FontVariant,
        "weigth": FontWeigth,
    }

    def __init__(self, **kwargs: Unpack[StyleParamTypes]) -> None:
        self.attributes = self.param_classes.copy()
        if "reference" in kwargs:
            ref_obj = kwargs["reference"]
            for attr in self.attributes:
                self.attributes[attr] = ref_obj.attributes[attr]
        for attr, _class in self.param_classes.items():
            if attr in kwargs:
                attr_obj = kwargs[attr]
                if not isinstance(attr_obj, _class):
                    attr_obj = _class(attr_obj)
                self.attributes[attr] = attr_obj
            elif "reference" not in kwargs:
                self.attributes[attr] = _class()

    def __str__(self) -> str:
        """
        SVG font style string
        """
        return_kvs = []
        for attr_v in self.attributes.values():
            if str(attr_v):
                return_kvs.append(str(attr_v))
        return ";".join(return_kvs)

    def copy(self) -> "Style":
        """
        Return an object with same atrributes.
        """
        obj = Style()
        for k, v in self.attributes.items():
            obj.attributes[k] = v.copy()
        return obj

    def merge(self, other: "Style") -> None:
        """
        Overwrite with all not 'None' values
        """
        # pylint: disable=singleton-comparison
        for k, o_attr in other.attributes.items():
            if isinstance(o_attr, StrokeDashArray):
                if o_attr.values != []:
                    self.attributes[k] = StrokeDashArray(o_attr.values)
            else:
                if o_attr.value != None:
                    self.attributes[k] = o_attr.copy()

    def diff(self, other: "Style") -> "Style":
        """
        Return style object with only attributes which are overwritten in 'other'
        """
        style = Style()
        for k, o_attr in other.attributes.items():
            if o_attr.isdefault:
                continue
            if isinstance(o_attr, StrokeDashArray):
                if o_attr.values not in ([], self.attributes[k].values):
                    style.attributes[k] = StrokeDashArray(o_attr.values)
            else:
                if not o_attr.isdefault and o_attr.value != self.attributes[k].value:
                    style.attributes[k] = o_attr.copy()

        return style

    @property
    def stroke_width(self) -> float | None:
        """
        Get stroke width value
        """
        return (
            None
            if self.attributes[  # pylint: disable=using-constant-test
                "stroke_width"
            ].isdefault
            else self.attributes["stroke_width"].value
        )
