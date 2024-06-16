"""
Module to define the basic Float classes.
"""

from typing import Union
from collections.abc import Iterable


class Float:
    """
    A Float is an object that has other Float objects as inputs and output.
    With Float you can build a loop-free directed graph for calculating
    dynamically float numbers.
    Float can be used with pyhton built-in arithmetic operations.
    """

    str_round = 3

    def __init__(self, value: Union["Float", float] = None) -> None:
        self._value = None
        self.inputs = []
        self.outputs = []
        self._float_ref = None
        if value is not None:
            self.float_ref = value

    @property
    def float_ref(self) -> "Float":
        """
        Get the reference Float object
        """
        return self._float_ref

    @float_ref.setter
    def float_ref(self, float_ref: "Float"):
        if isinstance(self._float_ref, Float):
            self.remove_input(self._float_ref)
        if isinstance(float_ref, Float):
            self._float_ref = float_ref
            self.add_input(self._float_ref)
        else:
            if hasattr(float_ref, "__float__"):
                self._float_ref = float_ref
            else:
                self._float_ref = float(float_ref)
            self.input_changed()

    @property
    def _get_value(self) -> float:
        if self._float_ref is None:
            raise TypeError("Object not fully initialized")
        return float(self._float_ref)

    @property
    def input_history(self) -> set["Float"]:
        """
        Get all inputs of all inputs recursively
        """
        input_history = set(self.inputs)
        for i in input_history:
            input_history.union(i.input_history)
        return input_history

    def add_input(self, other: "Float") -> None:
        """
        Add other Float object as a input
        """
        if self in other.input_history:
            raise RuntimeError("Input loop detected")
        self.inputs.append(other)
        other.outputs.append(self)
        self.input_changed()

    def remove_input(self, other: "Float") -> None:
        """
        Remove other Float object from inputs
        """
        self.inputs.remove(other)
        other.outputs.remove(self)
        self.input_changed()

    def add_output(self, other: "Float") -> None:
        """
        Add other Float object as a output
        """
        other.add_input(self)

    def remove_output(self, other: "Float") -> None:
        """
        Remove other Float object from outputs
        """
        other.remove_input(self)

    def my_input_changed(self):
        """
        Perform actions on input change
        """

    def input_changed(self):
        """
        Inform myself and all outputs about an input change
        """
        self.my_input_changed()
        for o in self.outputs:
            o.input_changed()

    def __str__(self):
        v = round(float(self), self.str_round)
        if v == 0:
            v = 0
        return f"{v:g}"

    def __float__(self):
        return self._get_value

    def __int__(self):
        return int(float(self))

    def __bool__(self):
        try:
            return bool(self._get_value)
        except TypeError:
            return False

    def __neg__(self):
        return Mul(value1=self, value2=-1)

    def __pos__(self):
        return Mul(value1=self, value2=1)

    @property
    def _i_action_value(self) -> "Float":
        if isinstance(self.float_ref, Float):
            return self.float_ref.float_ref
        return Float(self.float_ref)

    def __add__(self, other):
        return Sum(value1=self, value2=other)

    def __radd__(self, other):
        return Sum(value1=other, value2=self)

    def __sub__(self, other):
        return Sub(value1=self, value2=other)

    def __rsub__(self, other):
        return Sub(value1=other, value2=self)

    def __mul__(self, other):
        return Mul(value1=self, value2=other)

    def __rmul__(self, other):
        return Mul(value1=other, value2=self)

    def __div__(self, other):
        return Div(value1=self, value2=other)

    def __truediv__(self, other):
        return self.__div__(other)

    def __rdiv__(self, other):
        return Div(value1=other, value2=self)

    def __rtruediv__(self, other):
        return self.__rdiv__(other)

    def __floordiv__(self, other):
        return FloorDiv(value1=self, value2=other)

    def __rfloordiv__(self, other):
        return FloorDiv(value1=other, value2=self)

    def __mod__(self, other):
        return Mod(value1=self, value2=other)

    def __rmod__(self, other):
        return Mod(value1=other, value2=self)

    def __pow__(self, other):
        return Pow(value1=self, value2=other)

    def __rpow__(self, other):
        return Pow(value1=other, value2=self)


class FloatList:
    """
    List of Float values
    """

    name = "values"

    def __init__(self, values: Iterable[float | Float] = None) -> None:
        self._values = []
        if values is not None:
            self.values = values

    @property
    def values(self) -> list[Float]:
        """
        Get value list
        """
        return self._values

    @values.setter
    def values(self, values: Iterable[float | Float]) -> None:
        """
        Verify and set values
        """
        if not isinstance(values, list):
            raise TypeError(f"{self.name} must be a list of float values")
        for value in values:
            if not isinstance(value, Float):
                value = Float(value)
            self._values.append(value)

    def __str__(self) -> str:
        if not self.values:
            return ""
        return ",".join([str(value) for value in self.values])

    @property
    def isdefault(self) -> bool:
        """
        Check, if object's value is not set.
        """
        return self.values == []

    def equals(self, other) -> bool:
        """
        Check, if other's float value is equal to self's float value
        """
        for i, v in enumerate(self.values):
            if float(v) != float(other.values[i]):
                return False
        return True


class FloatProperty:
    """
    Property descriptor for Float objects.
    It automatically creates an intermediate Float object,
    which uses the given Float object as input.
    Or, if input is a python native float or int, it creates
    a Float object with that value and use it as the input.
    """

    def __init__(self):
        self.instances = {}

    def __get__(self, instance, owner):
        return self.instances[instance]

    def __set__(self, instance, f):
        if f is not isinstance(f, Float):
            f = Float(f)
        if instance not in self.instances:
            self.instances[instance] = f
        else:
            self.instances[instance].float_ref = f.float_ref


class FloatMath(Float):
    """
    Base class for all "calculated" Float classes
    """

    def __init__(self) -> None:
        super().__init__()
        self._value_cache = None

    def fill_cache(self) -> None:
        """
        Calculate the value for the cache
        """
        raise NotImplementedError

    @property
    def _get_value(self) -> float:
        if self._value_cache is None:
            self.fill_cache()
        return self._value_cache

    def my_input_changed(self):
        self._value_cache = None
        return super().my_input_changed()


class OneValueMath(FloatMath):
    """
    Base class for all arithmetic operations with two Float values
    """

    def __init__(self, value: Float | float) -> None:
        super().__init__()
        self.float_ref = value

    def fill_cache(self) -> None:
        """
        Calculate the value for the cache
        """
        raise NotImplementedError


class TwoValueMath(FloatMath):
    """
    Base class for all arithmetic operations with two Float values
    """

    def __init__(self, value1: Float | float, value2: Float | float) -> None:
        super().__init__()
        self.value1 = value1
        if isinstance(value1, Float):
            self.add_input(value1)
        self.value2 = value2
        if isinstance(value2, Float):
            self.add_input(value2)

    def fill_cache(self) -> None:
        """
        Calculate the value for the cache
        """
        raise NotImplementedError


class Sum(TwoValueMath):
    """
    Represent the sum of two referenced Float objects
    """

    def fill_cache(self) -> None:
        self._value_cache = float(self.value1) + float(self.value2)


class Sub(TwoValueMath):
    """
    Represent the substraction of two referenced Float objects
    """

    def fill_cache(self) -> None:
        self._value_cache = float(self.value1) - float(self.value2)


class Mul(TwoValueMath):
    """
    Represent the multiplication of two referenced Float objects
    """

    def fill_cache(self) -> None:
        self._value_cache = float(self.value1) * float(self.value2)


class Div(TwoValueMath):
    """
    Represent the division of two referenced Float objects
    """

    def fill_cache(self) -> None:
        self._value_cache = float(self.value1) / float(self.value2)


class FloorDiv(TwoValueMath):
    """
    Represent the integer value of a division of two referenced Float objects
    """

    def fill_cache(self) -> None:
        self._value_cache = float(self.value1) // float(self.value2)


class Mod(TwoValueMath):
    """
    Represent the value of a modulo division of two referenced Float objects
    """

    def fill_cache(self) -> None:
        self._value_cache = float(self.value1) % float(self.value2)


class Pow(TwoValueMath):
    """
    Represent the value of the power of two referenced Float objects
    """

    def fill_cache(self) -> None:
        self._value_cache = float(self.value1) ** float(self.value2)
