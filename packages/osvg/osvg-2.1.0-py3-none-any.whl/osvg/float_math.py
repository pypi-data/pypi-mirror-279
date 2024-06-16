"""
Module to define Float classes to calculate float numbers.
"""

from collections.abc import Iterable
from types import GeneratorType
import math
import osvg.float
import osvg.helper


class EmptyCalculatedListError(ValueError):
    """
    Exception indicating an access to the value of CalculatedList object,
    which has no float values added yet.
    """


class Cos(osvg.float.OneValueMath):
    """
    Cosinus value of an angle in degree
    """

    def fill_cache(self):
        self._value_cache = math.cos(osvg.helper.radians(float(self.float_ref)))


class Sin(osvg.float.OneValueMath):
    """
    Sinus value of an angle in degree
    """

    def fill_cache(self):
        self._value_cache = math.sin(osvg.helper.radians(float(self.float_ref)))


class Cot(osvg.float.OneValueMath):
    """
    Cotangent value of an angle in degree
    """

    def fill_cache(self):
        v = osvg.helper.radians(float(self.float_ref))
        self._value_cache = math.cos(v) / math.sin(v)


class Tan(osvg.float.OneValueMath):
    """
    Tangent value of an angle in degree
    """

    def fill_cache(self):
        v = osvg.helper.radians(float(self.float_ref))
        self._value_cache = math.sin(v) / math.cos(v)


class CalculatedList(osvg.float.FloatMath):
    """
    Base class for all calculated Floats with a list of Float objects
    """

    def __init__(
        self,
        *args: Iterable[osvg.float.Float | float],
    ) -> None:
        super().__init__()
        if args:
            self.add(args)

    @property
    def floats(self) -> list[float]:
        """
        Get tuple of all float input object values
        """
        if not self.inputs:
            raise EmptyCalculatedListError(f"{self.__class__.__name__} has no inputs")
        return tuple(float(x) for x in self.inputs)

    def add(
        self, f: osvg.float.Float | float | Iterable[osvg.float.Float | float]
    ) -> None:
        """
        Add a Float value or a iterable or a generator object with Float values
        """
        if not isinstance(f, (Iterable, GeneratorType)):
            f = [f]
        for v in f:
            if not issubclass(type(v), osvg.float.Float):
                v = osvg.float.Float(v)
            self.add_input(v)

    def fill_cache(self) -> None:
        raise NotImplementedError


class CalculatedKwargs(osvg.float.FloatMath):
    """
    Base class for all calculated Floats with keyword Float objects arguments
    """

    def __init__(
        self,
        **kwargs: osvg.float.Float | float,
    ) -> None:
        super().__init__()
        self.__dict__.update(kwargs)
        for k, v in kwargs.items():
            if not isinstance(v, osvg.float.Float):
                v = osvg.float.Float(v)
            kwargs[k] = v
            self.add_input(v)
        self.__dict__.update(kwargs)

    def fill_cache(self) -> None:
        raise NotImplementedError


class FunctFloat(CalculatedList):
    """
    Class for customized calculation of Floats by passing a external function
    """

    def __init__(
        self,
        args: Iterable[osvg.float.Float | float | int],
        funct: "function",
    ) -> None:
        super().__init__(*args)
        self.funct = funct

    def fill_cache(self) -> None:
        args = self.floats
        self._value_cache = self.funct(*args)


class Min(CalculatedList):
    """
    Get the lowest value of all given Floats.
    """

    def fill_cache(self) -> None:
        """
        Lowest values of all given values
        """
        self._value_cache = min(self.floats)


class LowestAbs(CalculatedList):
    """
    Return the floating number with the lowest absolute value.
    """

    def fill_cache(self) -> None:
        """
        Lowest absolute value of all given values
        """
        floats = self.floats
        self._value_cache = floats[0]
        for v in floats[1:]:
            if abs(v) < abs(self._value_cache):
                self._value_cache = v


class Max(CalculatedList):
    """
    Get the highest value of all given Floats.
    """

    def fill_cache(self) -> None:
        """
        Highest values of all given values
        """
        self._value_cache = max(self.floats)


class PercentOf(CalculatedKwargs):
    """
    Calculate percentage of a value
    """

    def __init__(
        self,
        reference: osvg.float.Float,
        percentage: float | osvg.float.Float,
        modulo: bool = False,
    ) -> None:
        super().__init__(reference=reference, percentage=percentage)
        self._modulo = False
        self.modulo = modulo

    @property
    def modulo(self) -> bool:
        """
        Get modulo value
        """
        return self._modulo

    @modulo.setter
    def modulo(self, _bool: bool) -> None:
        self._modulo = _bool
        self.input_changed()

    def fill_cache(self) -> None:
        # pylint: disable=no-member
        if self.modulo:
            self._value_cache = (
                float(self.reference) / 100 * (float(self.percentage) % 100)
            )
        else:
            self._value_cache = float(self.reference) / 100 * float(self.percentage)


class Int(osvg.float.OneValueMath):
    """
    Represents the integer value of a Float reference
    """

    def fill_cache(self) -> None:
        """
        Calculate the value for the cache
        """
        self._value_cache = int(float(self.float_ref))


class Abs(osvg.float.OneValueMath):
    """
    Represents the absulote value of a Float reference
    """

    def fill_cache(self) -> None:
        """
        Calculate the value for the cache
        """
        self._value_cache = abs(float(self.float_ref))


class Average(CalculatedList):
    """
    Represents the Average value of all Float references
    """

    def fill_cache(self) -> None:
        """
        Calculate the value for the cache
        """
        floats = self.floats
        self._value_cache = sum(floats) / len(floats)
