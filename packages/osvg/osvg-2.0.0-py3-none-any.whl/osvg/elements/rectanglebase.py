"""
Module to define shared methods for rectangle-like classes.
"""

from typing import Literal
from typing_extensions import Unpack
import osvg.elements.elementbase
import osvg.positions
import osvg.float
import osvg.float_math


class RectangleBaseParams(osvg.elements.elementbase.SVGElementParams):
    """
    Keyword argument definition for RectangleBase class.
    """

    width: float | osvg.float.Float = 0
    height: float | osvg.float.Float = 0


class RectangleBase(osvg.elements.elementbase.SVGElement):
    # pylint: disable=no-member
    """
    Base class for rectangle-like Elements.
    """
    width = osvg.float.FloatProperty()
    height = osvg.float.FloatProperty()

    def __init__(self, **kwargs: Unpack[RectangleBaseParams]) -> None:
        super().__init__(**kwargs)
        self.width = kwargs.get("width", 0)
        self.height = kwargs.get("height", 0)
        self.create_default_connectors()

    def _connector_top_left(self):
        return self.position - osvg.Position(self.width, self.height) / 2

    def _connector_top_center(self):
        return osvg.positions.YShiftedPosition(
            origin=self.position,
            y_shift=self.height / -2,
        )

    def _connector_top_right(self):
        return self.position + osvg.Position(self.width / 2, self.height / -2)

    def _connector_center_left(self):
        return osvg.positions.XShiftedPosition(
            origin=self.position,
            x_shift=self.width / -2,
        )

    def _connector_center(self):
        return osvg.positions.Position(self.position.x, self.position.y)

    def _connector_center_right(self):
        return osvg.positions.XShiftedPosition(
            origin=self.position,
            x_shift=self.width / 2,
        )

    def _connector_bottom_left(self):
        return self.position + osvg.Position(self.width / -2, self.height / 2)

    def _connector_bottom_center(self):
        return osvg.positions.YShiftedPosition(
            origin=self.position,
            y_shift=self.height / 2,
        )

    def _connector_bottom_right(self):
        return self.position + osvg.Position(self.width, self.height) / 2

    def create_default_connectors(self) -> None:
        """
        Create Positions as connectors and add them.
        """
        self.add_connector(
            self._connector_top_left(), name="top-left", respect_rotation=True
        )
        self.add_connector(
            self._connector_top_center(), name="top-center", respect_rotation=True
        )
        self.add_connector(
            self._connector_top_right(), name="top-right", respect_rotation=True
        )
        self.add_connector(
            self._connector_center_left(), name="center-left", respect_rotation=True
        )
        self.add_connector(self._connector_center(), "center")
        self.add_connector(
            self._connector_center_right(), name="center-right", respect_rotation=True
        )
        self.add_connector(
            self._connector_bottom_left(), name="bottom-left", respect_rotation=True
        )
        self.add_connector(
            self._connector_bottom_center(), name="bottom-center", respect_rotation=True
        )
        self.add_connector(
            self._connector_bottom_right(), name="bottom-right", respect_rotation=True
        )

    def add_connector_at_angle(self, angle: float | osvg.float.Float, name: str):
        """
        Add a connector at element's border at the angle
        in relation to the center.
        """
        # pylint: disable=too-many-return-statements,too-many-branches
        if name in self.connectors:
            raise ValueError(f"Connector with name {name} already exists")
        if isinstance(angle, osvg.float.Float):
            angle = float(angle)
        n_angle = angle % 360
        if n_angle == 0:
            self.connectors[name] = self.connectors["center-right"]
        else:
            if n_angle > 180:
                half_height = self.height / -2
            else:
                half_height = self.height / 2
            if 90 < n_angle < 270:
                half_width = self.width / -2
            else:
                half_width = self.width / 2
            cot_angle = -osvg.float_math.Cot(angle)
            x_shift = osvg.float_math.LowestAbs(
                half_width,
                cot_angle * half_height,
            )
            tan_angle = -osvg.float_math.Tan(angle)
            y_shift = osvg.float_math.LowestAbs(
                half_height,
                tan_angle * half_width,
            )
            self.add_connector(
                position=self.position + (x_shift, y_shift),
                name=name,
                respect_rotation=True,
            )
        return self.connectors[name]

    def add_side_connector(
        self,
        name: str,
        side: Literal["top", "right", "bottom", "left"],
        percentage: float | osvg.float.Float = 50,
    ):
        """
        Add a connector at element's border on given side at the percent of the side's length.
        Percent will be modulo of 100. (-10 => 90; 110 => 10)
        Percent at top/bottom: 0 is left, 100 is right
        Percent at left/right: 0 is bottom, 100 is top
        """
        # pylint: disable=too-many-return-statements,too-many-branches
        if side in ["top", "bottom"]:
            x_shift = (
                osvg.float_math.PercentOf(
                    reference=self.width, percentage=percentage, modulo=True
                )
                - self.width / 2
            )  # Percent of width minus half width
            y_shift = self.height / 2
            if side == "top":
                y_shift = -y_shift
        elif side in ["left", "right"]:
            x_shift = self.width / 2
            if side == "left":
                x_shift = -x_shift
            y_shift = (
                osvg.float_math.PercentOf(
                    reference=self.height, percentage=percentage, modulo=True
                )
                - self.height / 2
            )  # Percent of heigth minus half heigth
        return self.add_connector(
            position=self.position + (x_shift, y_shift),
            name=name,
            respect_rotation=True,
        )
