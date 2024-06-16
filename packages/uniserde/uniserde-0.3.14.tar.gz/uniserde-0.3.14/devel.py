from __future__ import annotations

from typing import *  # type: ignore
from dataclasses import dataclass
import uniserde
from pathlib import Path


value_raw = Path.home()
value_serialized = uniserde.as_json(value_raw)
print(value_serialized)

value_parsed = uniserde.from_json(value_serialized, Path)
print(value_parsed)


def foo():
    @dataclass
    class Minimum:
        minimum_value: float

    # class Constraint:
    #     def __init__(self, *args, **kwargs) -> None:
    #         pass

    #     @staticmethod
    #     def __call__(*args, **kwargs) -> Any:
    #         pass

    T = TypeVar("T")
    Tup = TypeVarTuple("Tup")

    # Constraint = Annotated[T, Tup]
    Constraint: TypeAlias = Annotated

    MnimumAnn = Annotated[T, Minimum(0.0)]

    class Foo:
        float_value: float

        int_value: Constraint[
            int,
            Minimum(0),
        ]
