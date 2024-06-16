"""
Module to define position objects.
"""

# pylint: disable=missing-function-docstring

import math
from collections.abc import Iterable
import osvg.float
import osvg.float_math
import osvg.helper


class Position:
    """
    Class to define a point within in the two-dimensional drawing.
    'x' is the floating point value on the x axis with
    x=0 as the most left point and x>0 is moving to the right.
    'y' is the floating point value on the y axis with
    y=0 as the most upper point and y>0 is moving down.

    A PositionObject is a linkable object.
    """

    # pylint: disable=too-few-public-methods

    str_round = 3
    x = osvg.float.FloatProperty()
    y = osvg.float.FloatProperty()

    def __init__(
        self,
        x: osvg.float.Float | float = 0.0,
        y: osvg.float.Float | float = 0.0,
    ) -> None:
        self.x = x
        self.y = y

    def __str__(self):
        """
        Get the SVG string
        """
        return f"{self.x},{self.y}"

    @staticmethod
    def __clean_other(other):
        if not isinstance(other, Position):
            if isinstance(other, Iterable):
                return Position(*other)
            return Position(other, other)
        return other

    def __add__(self, other):
        other = self.__clean_other(other)
        return Position(x=self.x + other.x, y=self.y + other.y)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = self.__clean_other(other)
        return Position(x=self.x - other.x, y=self.y - other.y)

    def __rsub__(self, other):
        other = self.__clean_other(other)
        return Position(x=other.x - self.x, y=other.y - self.y)

    def __mul__(self, other):
        other = self.__clean_other(other)
        return Position(x=self.x * other.x, y=self.y * other.y)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        other = self.__clean_other(other)
        return Position(x=self.x / other.x, y=self.y / other.y)

    def __truediv__(self, other):
        return self.__div__(other)

    def __rdiv__(self, other):
        other = self.__clean_other(other)
        return Position(x=other.x / self.x, y=other.y / self.y)

    def __rtruediv__(self, other):
        return self.__div__(other)

    def __floordiv__(self, other):
        other = self.__clean_other(other)
        return Position(x=self.x // other.x, y=self.y // other.y)

    def __rfloordiv__(self, other):
        other = self.__clean_other(other)
        return Position(x=other.x // self.x, y=other.y // self.y)

    def __mod__(self, other):
        other = self.__clean_other(other)
        return Position(x=self.x % other.x, y=self.y % other.y)

    def __rmod__(self, other):
        other = self.__clean_other(other)
        return Position(x=other.x % self.x, y=other.y % self.y)

    def __pow__(self, other):
        other = self.__clean_other(other)
        return Position(x=self.x**other.x, y=self.y**other.y)

    def __rpow__(self, other):
        other = self.__clean_other(other)
        return Position(x=other.x**self.x, y=other.y**self.y)


class PositionProperty:
    """
    Property descriptor for Position objects
    """

    def __init__(self):
        self.instances = {}

    def __get__(self, instance, owner):
        return self.instances[instance]

    def __set__(
        self, instance, p: Position | Iterable[osvg.float.Float | float] = None
    ):
        if p is None:
            x = 0
            y = 0
        elif issubclass(type(p), Position):
            x = p.x
            y = p.y
        elif isinstance(p, Iterable):
            x = p[0]
            y = p[1]
        else:
            raise TypeError("Position object required")
        if instance not in self.instances:
            self.instances[instance] = Position()
        self.instances[instance].x = x
        self.instances[instance].y = y


class XShiftedPosition(Position):
    # pylint: disable=too-few-public-methods
    """
    A relative position object where the x coordinate is shifted
    by the given float or to the x value of the given position.
    """

    def __init__(
        self,
        origin: Position,
        x_shift: Position | osvg.float.Float | float = 0,
    ) -> None:
        if not isinstance(origin, Position):
            if isinstance(origin, Iterable):
                origin = Position(*origin)
            else:
                origin = Position(origin, origin)
        if isinstance(x_shift, Position):
            x = x_shift.x
        elif isinstance(x_shift, Iterable):
            x = Position(*x_shift).x
        else:
            x = origin.x + x_shift
        super().__init__(x=x, y=origin.y)


class YShiftedPosition(Position):
    # pylint: disable=too-few-public-methods
    """
    A relative position object where the y coordinate is shifted
    by the given float or to the y value of the given position.
    """

    def __init__(
        self,
        origin: Position,
        y_shift: Position | osvg.float.Float | float = 0,
    ) -> None:
        if not isinstance(origin, Position):
            if isinstance(origin, Iterable):
                origin = Position(*origin)
            else:
                origin = Position(origin, origin)
        if isinstance(y_shift, Position):
            y = y_shift.y
        elif isinstance(y_shift, Iterable):
            y = Position(*y_shift).y
        else:
            y = origin.y + y_shift
        super().__init__(x=origin.x, y=y)


class Distance(osvg.float_math.CalculatedKwargs):
    """
    Class to provide a calculated Float object representing the
    distance between two Positions
    """

    def __init__(self, a: Position, b: Position) -> None:
        super().__init__(ax=a.x, ay=a.y, bx=b.x, by=b.y)

    def fill_cache(self) -> None:
        # pylint: disable=no-member
        self._value_cache = math.dist(
            [float(self.ax), -float(self.ay)],
            [float(self.bx), -float(self.by)],
        )


class AngleDegree(osvg.float_math.CalculatedKwargs):
    """
    Class to provide a calculated Float object representing the
    angle from "a" to another position "b" in radians
    """

    def __init__(self, a: Position, b: Position) -> None:
        super().__init__(ax=a.x, ay=a.y, bx=b.x, by=b.y)

    def fill_cache(self) -> None:
        # pylint: disable=no-member
        dx = float(self.bx) - float(self.ax)
        dy = float(self.ay) - float(self.by)  # due to the inverted y-axis
        self._value_cache = osvg.helper.degrees(math.atan2(dy, dx))


class XonCircle(osvg.float_math.CalculatedKwargs):
    """
    Class to provide a calculated Float object representing the
    x value of a position on a circle.
    Note: angle=0 is twelve o'clock and it goes clockwise.
    """

    def __init__(self, angle: osvg.float.Float, radius: osvg.float.Float) -> None:
        super().__init__(angle=angle, radius=radius)

    def fill_cache(self) -> float:
        # pylint: disable=no-member
        self._value_cache = math.cos(osvg.helper.radians(float(self.angle))) * float(
            self.radius
        )


class YonCircle(osvg.float_math.CalculatedKwargs):
    """
    Class to provide a calculated osvg.float.Float object representing the
    y value of a position on a circle.
    Note: angle=0 is twelve o'clock and it goes clockwise.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, angle: osvg.float.Float, radius: osvg.float.Float) -> None:
        super().__init__(angle=angle, radius=radius)

    def fill_cache(self) -> float:
        # pylint: disable=no-member
        self._value_cache = math.sin(osvg.helper.radians(float(self.angle))) * -float(
            self.radius
        )


class XonEllipse(osvg.float_math.CalculatedKwargs):
    """
    Class to provide a calculated Float object representing the
    x value of a position on a ellipse.
    Note: angle=0 is twelve o'clock and it goes clockwise.
    """

    def __init__(
        self,
        angle: osvg.float.Float,
        radius_x: osvg.float.Float,
        radius_y: osvg.float.Float,
    ) -> None:
        super().__init__(angle=angle, radius_x=radius_x, radius_y=radius_y)

    def fill_cache(self) -> float:
        # pylint: disable=no-member
        self._value_cache = abs(
            float(self.radius_x)
            * float(self.radius_y)
            / math.sqrt(
                float(self.radius_y) ** 2
                + float(self.radius_x) ** 2
                * math.tan(osvg.helper.radians(float(self.angle))) ** 2
            )
        )
        if 90 < float(self.angle) % 360 < 270:
            self._value_cache = -1 * self._value_cache


class YonEllipse(osvg.float_math.CalculatedKwargs):
    """
    Class to provide a calculated Float object representing the
    y value of a position on a ellipse.
    Note: angle=0 is twelve o'clock and it goes clockwise.
    """

    def __init__(
        self,
        angle: osvg.float.Float,
        radius_x: osvg.float.Float,
        radius_y: osvg.float.Float,
    ) -> None:
        super().__init__(angle=angle, radius_x=radius_x, radius_y=radius_y)

    def fill_cache(self) -> float:
        # pylint: disable=no-member
        tan = math.tan(osvg.helper.radians(float(self.angle)))
        if tan == 0:
            self._value_cache = 0.0
        else:
            self._value_cache = abs(
                float(self.radius_x)
                * float(self.radius_y)
                / math.sqrt(
                    float(self.radius_x) ** 2
                    + float(self.radius_y) ** 2
                    / math.tan(osvg.helper.radians(float(self.angle))) ** 2
                )
            )
            if float(self.angle) % 360 > 180:
                self._value_cache = -1 * self._value_cache


class RotatedPosition(Position):
    """
    Class to define a point rotated around another point by an angle.
    'reference' is the Position which should be shifted.
    'center' is the center of the circle with 'parent' on the cirle track.

    Note:
    - angle goes clockwise
    - angle is delta to current angle 'reference' -> 'parent'
    """

    # pylint: disable=too-few-public-methods

    x = osvg.float.FloatProperty()
    y = osvg.float.FloatProperty()
    origin = PositionProperty()
    center = PositionProperty()
    angle = osvg.float.FloatProperty()

    def __init__(
        self,
        origin: Position,
        center: Position,
        angle: osvg.float.Float | float = 0,
    ) -> None:
        super().__init__()
        self.origin = origin
        self.center = center
        self.angle = angle

        distance = Distance(self.center, self.origin)
        new_angle = self.angle + AngleDegree(self.center, self.origin)

        # Calc x
        new_shift_x = XonCircle(angle=new_angle, radius=distance)
        self.x = self.center.x + new_shift_x

        # Calc y
        new_shift_y = YonCircle(angle=new_angle, radius=distance)
        self.y = self.center.y + new_shift_y


class PolarShiftedPosition(Position):
    """
    Class to define a position which is described by a polar coordinate
    with the reference position as center.
    """

    # pylint: disable=too-few-public-methods

    x = osvg.float.FloatProperty()
    y = osvg.float.FloatProperty()
    origin = PositionProperty()
    angle = osvg.float.FloatProperty()
    distance = osvg.float.FloatProperty()
    x_shift = osvg.float.FloatProperty()
    y_shift = osvg.float.FloatProperty()

    def __init__(
        self,
        origin: Position,
        angle: osvg.float.Float | float = 0,
        distance: osvg.float.Float | float = 0,
    ) -> None:
        super().__init__()
        self.origin = origin
        self.angle = angle
        self.distance = distance

        x_shift = osvg.float_math.Cos(self.angle) * self.distance
        self.x = origin.x + x_shift
        y_shift = -osvg.float_math.Sin(self.angle) * self.distance
        self.y = origin.y + y_shift


class RayCrossCirclePosition(Position):
    """
    Class to define a point at which a ray from
    circle center to a position crosses the circle.
    """

    # pylint: disable=too-few-public-methods

    x = osvg.float.FloatProperty()
    y = osvg.float.FloatProperty()
    center = PositionProperty()
    position = PositionProperty()
    radius = osvg.float.FloatProperty()
    x_shift = osvg.float.FloatProperty()
    y_shift = osvg.float.FloatProperty()

    def __init__(
        self,
        center: Position,
        position: Position,
        radius: osvg.float.Float | float,
    ) -> None:
        super().__init__()
        self.center = center
        self.position = position
        self.radius = radius

        angle = AngleDegree(a=self.center, b=self.position)
        self.x = center.x + XonCircle(angle=angle, radius=self.radius)
        self.y = center.y + YonCircle(angle=angle, radius=self.radius)
