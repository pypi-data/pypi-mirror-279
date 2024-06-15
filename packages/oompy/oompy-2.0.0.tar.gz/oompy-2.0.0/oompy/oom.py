from enum import Enum
from fractions import Fraction
from typing import Union, Dict
import matplotlib.units as units
import sympy as sp
import numpy as np

from .utils import Stringize, ParseUnit, StripCoeff, JoinUnits
from .constants import ConstantValues
from .units import (
    Type,
    CGSUnits,
    GetBaseType,
    ConvertUnit,
    RaiseUnitsToPower,
    Powers,
    BaseUnits,
    LatexUnitMapping,
    UnitEquivalencies,
)


ValidQuantity = Union["Quantity", tuple, int, float, np.ndarray]


class Quantity:
    def __init__(self, *args) -> None:
        if (len(args) == 1) and isinstance(args[0], Quantity):
            self.value = args[0].value  # type: float
            self.unit = args[0].unit  # type: str
        elif (len(args) == 1) and isinstance(args[0], str):
            self.value, self.unit = StripCoeff(args[0])
        elif (len(args) == 1) and isinstance(args[0], (int, float)):
            self.value = args[0]
            self.unit = ""
        elif (
            (len(args) == 2)
            and isinstance(args[0], (int, float))
            and isinstance(args[1], str)
        ):
            self.value = args[0]
            self.unit = args[1]
        else:
            raise Exception("Invalid arguments for Quantity.__init__")
        self.assumption = None  # type: Union[Assumptions, None]

    @property
    def cgs(self) -> "Quantity":
        return self >> Stringize(
            {CGSUnits[b]: p for b, p in GetBaseType(self.unit).items()}
        )

    def __to(self, unit: str) -> "Quantity":
        if unit == "CGS":
            return self.cgs
        target = Quantity(unit)
        if ~self == ~target:
            return Quantity(*ConvertUnit(Stringize((self.value, self.unit)), unit))
        elif self.assumption is None:
            raise Exception(
                "Cannot convert between different base types (no assumption)"
            )
        elif self.assumption == Assumptions.Light:
            return ConvertAssuming_Light(self, target)
        elif self.assumption == Assumptions.Thermal:
            return ConvertAssuming_Thermal(self, target)
        elif self.assumption == Assumptions.Redshift:
            return ConvertAssuming_Redshift(self, target)
        raise Exception(
            f"Cannot convert from {~self} to {~target} with the assumption of {self.assumption}"
        )

    def __repr__(self) -> str:
        return f"{self.value} {self.unit}"

    def value_latex(self) -> str:
        if self.value < 0.001 or self.value > 9999:
            nval = f"{self.value:.5e}".split("e")
        else:
            nval = f"{self.value:.5f}".split("e")
        return nval[0] + (
            f"\\cdot 10^{{{int(nval[1])}}}"
            if len(nval) > 1 and int(nval[1]) != 0
            else ""
        )

    def unit_latex(self) -> str:
        units = [f.split("^")[0] for f in self.unit.split(" ")]
        units_ = []
        for u in units:
            for k, v in LatexUnitMapping.items():
                u = u.replace(k, v)
            units_.append(u)
        units = units_
        pows = [
            (f"{{}}^{{{f.split(" ^ ")[1]}}}" if len(f.split("^")) > 1 else "")
            for f in self.unit.split(" ")
        ]
        units = [
            u if "_" in u else f"\\text{{{u}}}" + p
            for u, p in zip(units, pows)
            if u != ""
        ]
        return "~".join(units)

    def _repr_latex_(self) -> str:
        nval = self.value_latex()
        units = self.unit_latex()
        if units != "":
            return f"${nval}~[" + units + "]$"
        else:
            return f"${nval}$"

    def __str__(self) -> str:
        return self.__repr__()

    def __hash__(self) -> int:
        return hash(self.cgs.value)

    def __format__(self, format_spec: str) -> str:
        if GetBaseType(self.unit) == GetBaseType(""):
            return f"{self.value:{format_spec}}"
        else:
            return f"{self.value:{format_spec}} {self.unit}"

    def __invert__(self) -> Dict["Type", "Fraction"]:
        return GetBaseType(self.unit)

    def __eq__(self, other) -> bool:
        if isinstance(other, Quantity):
            return (self.__invert__() == ~other) and (self.cgs.value == other.cgs.value)
        elif isinstance(other, tuple):
            return self.value == Quantity(*other)
        elif isinstance(other, (int, float)):
            return (self.cgs.value == other) and (
                ParseUnit(self.cgs.unit) == ParseUnit("")
            )
        else:
            raise Exception("Invalid type for Quantity.__eq__")

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other) -> bool:
        if isinstance(other, Quantity):
            if ~other != self.__invert__():
                raise Exception("Cannot compare different base types")
            return self.cgs.value < other.cgs.value
        elif isinstance(other, tuple):
            return self < Quantity(*other)
        elif isinstance(other, (int, float)):
            if self.unit != "":
                raise Exception("Cannot compare different base types")
            return self.cgs.value < other
        else:
            raise Exception("Invalid type for Quantity.__lt__")

    def __le__(self, other) -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other) -> bool:
        return not self.__le__(other)

    def __ge__(self, other) -> bool:
        return not self.__lt__(other)

    def __rshift__(self, unit: Union[str, "Quantity", "Assumptions"]) -> "Quantity":
        if isinstance(unit, Quantity):
            return self >> unit.unit
        elif isinstance(unit, str):
            return self.__to(unit)
        elif isinstance(unit, Assumptions):
            self.assume(unit)
            return self
        elif self.unit == unit:
            return self
        else:
            raise Exception("Invalid unit")

    def __add__(self, other: ValidQuantity) -> "Quantity":
        if isinstance(other, Quantity):
            if self.unit == other.unit:
                return Quantity(self.value + other.value, self.unit)
            else:
                return self + (other >> self.unit)
        elif isinstance(other, tuple):
            return self + Quantity(*other)
        elif isinstance(other, (int, float)):
            assert self.unit == "", "Invalid arguments for Quantity.__add__"
            return Quantity(self.value + other, self.unit)
        else:
            raise Exception("Invalid arguments for Quantity.__add__")

    def assume(self, assumption: "Assumptions") -> None:
        self.assumption = assumption

    def __radd__(self, other: ValidQuantity) -> "Quantity":
        return self + other

    def __neg__(self) -> "Quantity":
        return Quantity(-self.value, self.unit)

    def __abs__(self) -> "Quantity":
        return Quantity(abs(self.value), self.unit)

    def __sub__(self, other: ValidQuantity) -> "Quantity":
        return self + (-Quantity(other))

    def __rsub__(self, other: ValidQuantity) -> "Quantity":
        return (-self) + other

    def __mul__(self, other: ValidQuantity) -> "Quantity":
        if isinstance(other, Quantity):
            return Quantity(
                self.value * other.value, JoinUnits(" ".join([self.unit, other.unit]))
            )
        elif isinstance(other, tuple):
            return self * Quantity(*other)
        elif isinstance(other, (int, float)):
            return Quantity(self.value * other, self.unit)
        elif isinstance(other, np.ndarray):
            return other * self
        else:
            raise Exception("Invalid arguments for Quantity.__mul__")

    def __rmul__(self, other: ValidQuantity) -> "Quantity":
        return self * other

    def __pow__(self, other: ValidQuantity) -> "Quantity":
        if isinstance(other, Quantity):
            assert other.unit == "", "Invalid arguments for Quantity.__pow__"
            return self ** (other.value)
        elif isinstance(other, tuple):
            return self ** Quantity(*other)
        elif isinstance(other, (int, float)):
            return Quantity(self.value**other, RaiseUnitsToPower(self.unit, other))
        else:
            raise Exception("Invalid arguments for Quantity.__pow__")

    def __truediv__(self, other: ValidQuantity) -> "Quantity":
        return self * (Quantity(other) ** (-1))

    def __rtruediv__(self, other: ValidQuantity) -> "Quantity":
        return (self ** (-1)) * other

    def __float__(self) -> float:
        return self.value


class MplUnitConverter(units.ConversionInterface):
    @staticmethod
    def convert(value, unit, axis):
        if isinstance(value, Quantity):
            return value.value
        elif isinstance(value, list):
            return [(v >> value[0].unit).value for v in value]
        elif isinstance(value, np.ndarray):
            return np.array([(v >> value[0].unit).value for v in value])

    @staticmethod
    def axisinfo(unit, axis):
        return units.AxisInfo(label=str(unit))

    @staticmethod
    def default_units(x, axis):
        if isinstance(x, Quantity):
            return f"${x.unit_latex()}$"
        elif isinstance(x, list) or isinstance(x, np.ndarray):
            return f"${x[0].unit_latex()}$"


class UnitsClass:
    def __init__(self) -> None:
        allunits = [
            [p + u for p in [""] + list(Powers.keys())]
            for u in list(BaseUnits.values()) + list(UnitEquivalencies.keys())
            if u != ""
        ]
        self.units = {u: Quantity(u) for u in sum(allunits, [])}

    def __getattribute__(self, name):
        if name == "all":
            return list(BaseUnits.values()) + list(UnitEquivalencies.keys())
        else:
            return super().__getattribute__("units")[name]


class Assumptions(Enum):
    Light = 0
    Thermal = 1
    Redshift = 2


class ConstantsClass:
    def __init__(self) -> None:
        self.constants = {k: Quantity(*v) for k, v in ConstantValues.items()}

    def __getattribute__(self, name):
        if name == "all":
            return {k: Quantity(*v).cgs for k, v in ConstantValues.items()}
        else:
            return super().__getattribute__("constants")[name]


def ConvertAssuming_Light(source: "Quantity", target: "Quantity") -> "Quantity":
    Constants = ConstantsClass()
    Units = UnitsClass()
    unit = target.unit
    if ~target == ~Quantity("erg"):
        if ~source == ~Quantity("Hz"):
            return (Constants.h * source) >> (unit)
        elif ~source == ~Quantity("cm"):
            return (Constants.h * Constants.c / source) >> (unit)
        elif ~source == ~Quantity("Hz rad"):
            return (Constants.hbar * source / Units.rad) >> (unit)
    elif ~target == ~Quantity("Hz"):
        if ~source == ~Quantity("erg"):
            return (source / Constants.h) >> (unit)
        elif ~source == ~Quantity("cm"):
            return (Constants.c / source) >> (unit)
    elif ~target == ~Quantity("cm"):
        if ~source == ~Quantity("erg"):
            return (Constants.h * Constants.c / source) >> (unit)
        elif ~source == ~Quantity("Hz"):
            return (Constants.c / source) >> (unit)
        elif ~source == ~Quantity("Hz rad"):
            return (Constants.c * Units.rad / source) >> (unit)
    raise Exception("Cannot convert between different base types")


def ConvertAssuming_Thermal(source: "Quantity", target: "Quantity") -> "Quantity":
    Constants = ConstantsClass()
    unit = target.unit
    if ~target == ~Quantity("erg"):
        if ~source == ~Quantity("K"):
            return (Constants.k_B * source) >> (unit)
    elif ~target == ~Quantity("K"):
        if ~source == ~Quantity("erg"):
            return (source / Constants.k_B) >> (unit)
    raise Exception("Cannot convert between different base types")


def ConvertAssuming_Redshift(source: "Quantity", target: "Quantity") -> "Quantity":
    import scipy.integrate as integrate  # type: ignore
    from scipy.optimize import fsolve  # type: ignore
    import math

    def integrand(x):
        return 1 / math.sqrt(
            Constants.omega_Matter.value * (1 + x) ** 3 + Constants.omega_Lambda.value
        )

    Constants = ConstantsClass()
    unit = target.unit
    if ~target == ~Quantity("cm"):
        assert ~source == ~Quantity("")

        return (Constants.c / Constants.H_0) * integrate.quad(
            integrand,
            0,
            (source >> "").value,
        )[0] >> (unit)
    elif ~target == ~Quantity(""):
        assert ~source == ~Quantity("cm")

        def func(Z):
            return (Constants.c / Constants.H_0 >> "Gpc").value * integrate.quad(
                integrand, 0, Z[0]
            )[0] - (source >> "Gpc").value

        return Quantity(fsolve(func, 1)[0], "")
    raise Exception("Cannot convert between different base types")
