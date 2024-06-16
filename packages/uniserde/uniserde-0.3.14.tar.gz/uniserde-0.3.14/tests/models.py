import enum
from dataclasses import KW_ONLY, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import *  # type: ignore

from uniserde import BsonDoc, JsonDoc, ObjectId, Serde, as_child


class RegularEnum(enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3


class FlagEnum(enum.Flag):
    ONE = 1
    TWO = 2
    FOUR = 4


@dataclass
class SimpleClass(Serde):
    foo: int
    bar: str


@dataclass
class TestClass(Serde):
    val_bool: bool
    val_int: int
    val_float: float
    val_bytes: bytes
    val_str: str
    val_datetime: datetime
    val_timedelta: timedelta
    val_tuple: tuple[int, str]
    val_list: list[int]
    val_set: Set[int]
    val_dict: dict[str, int]
    val_optional: Optional[int]
    val_old_union_optional_1: Union[int, None]
    val_old_union_optional_2: Union[None, int]
    val_new_union_optional_1: int | None
    val_new_union_optional_2: None | int
    val_any: Any
    val_object_id: ObjectId
    val_literal: Literal["one", "two", "three"]
    val_enum: RegularEnum
    val_flag: FlagEnum
    val_path: Path

    @classmethod
    def create_variant_1(cls) -> "TestClass":
        return cls(
            val_bool=True,
            val_int=1,
            val_float=1.0,
            val_bytes=b"these are bytes",
            val_str="this is a string",
            val_datetime=datetime(2020, 1, 2, tzinfo=timezone.utc),
            val_timedelta=timedelta(days=1, seconds=2, microseconds=3),
            val_tuple=(1, "one"),
            val_list=[1, 2, 3],
            val_set={1, 2, 3},
            val_dict={"one": 1, "two": 2},
            val_optional=1,
            val_old_union_optional_1=1,
            val_old_union_optional_2=1,
            val_new_union_optional_1=1,
            val_new_union_optional_2=1,
            val_any="this is an ANY value",
            val_object_id=ObjectId("62bd611fa847c71f1b68fffb"),
            val_literal="one",
            val_enum=RegularEnum.ONE,
            val_flag=FlagEnum.ONE | FlagEnum.TWO,
            val_path=Path.home() / "one",
        )

    @classmethod
    def create_variant_2(cls) -> "TestClass":
        return cls(
            val_bool=False,
            val_int=2,
            val_float=2.0,
            val_bytes=b"these are different bytes",
            val_str="this is another string",
            val_datetime=datetime(2024, 5, 6, tzinfo=timezone.utc),
            val_timedelta=timedelta(days=10, seconds=20, microseconds=30),
            val_tuple=(2, "two"),
            val_list=[4, 5, 6],
            val_set={4, 5, 6},
            val_dict={"three": 3, "four": 4},
            val_optional=None,
            val_old_union_optional_1=None,
            val_old_union_optional_2=None,
            val_new_union_optional_1=None,
            val_new_union_optional_2=None,
            val_any="this is another ANY value",
            val_object_id=ObjectId("62bd6122a847c71f1b68fffc"),
            val_literal="two",
            val_enum=RegularEnum.TWO,
            val_flag=FlagEnum.ONE | FlagEnum.TWO | FlagEnum.FOUR,
            val_path=Path.home() / "two",
        )


@dataclass
@as_child
class ParentClass(Serde):
    parent_int: int
    parent_float: float

    @classmethod
    def create_parent_variant_1(cls) -> "ParentClass":
        return cls(
            parent_int=1,
            parent_float=1.0,
        )


@dataclass
class ChildClass(ParentClass):
    child_float: float
    child_str: str

    @classmethod
    def create_child_variant_1(cls) -> "ChildClass":
        return cls(
            parent_int=1,
            parent_float=1.0,
            child_float=1.0,
            child_str="this is a string",
        )


@dataclass
class ClassWithId(Serde):
    id: int
    foo: int

    @classmethod
    def create(cls) -> "ClassWithId":
        return cls(1, 2)


@dataclass
class ClassWithKwOnly(Serde):
    foo: int

    _: KW_ONLY

    bar: int

    @classmethod
    def create(cls) -> "ClassWithKwOnly":
        return cls(1, bar=2)


@dataclass
class ClassWithStaticmethodOverrides(Serde):
    """
    Class which has uniserde's special methods overridden. This allows to check
    that they are called rather than the default.

    All methods are overridden as @staticmethod.
    """

    value: str
    format: str

    @classmethod
    def create(cls) -> "ClassWithStaticmethodOverrides":
        return cls("stored value", "python")

    def as_json(
        self,
        *,
        as_type: Optional[Type] = None,
        custom_serializers: dict[Type, Callable[[Any], Any]] = {},
    ) -> JsonDoc:
        return {"value": "overridden value", "format": "json"}

    def as_bson(
        self,
        *,
        as_type: Optional[Type] = None,
        custom_serializers: dict[Type, Callable[[Any], Any]] = {},
    ) -> BsonDoc:
        return {"value": "overridden value", "format": "bson"}

    @staticmethod
    def from_json(
        document: dict[str, Any],
        custom_deserializers: dict[Type, Callable[[Any], Any]] = {},
    ) -> "ClassWithStaticmethodOverrides":
        return ClassWithStaticmethodOverrides("overridden value", "json")

    @staticmethod
    def from_bson(
        document: dict[str, Any],
        custom_deserializers: dict[Type, Callable[[Any], Any]] = {},
    ) -> "ClassWithStaticmethodOverrides":
        return ClassWithStaticmethodOverrides("overridden value", "bson")

    @staticmethod
    def as_mongodb_schema(
        custom_handlers: dict[Type, Callable[[Any], Any]] = {},
    ) -> Any:
        return {"value": "overridden value", "format": "mongodb schema"}


@dataclass
class ClassWithClassmethodOverrides(Serde):
    """
    Same as the class above, but with the methods overridden as @classmethod.
    """

    value: str
    format: str

    @classmethod
    def create(cls) -> "ClassWithClassmethodOverrides":
        return cls("stored value", "python")

    @classmethod
    def from_json(
        cls,
        document: dict[str, Any],
        custom_deserializers: dict[Type, Callable[[Any], Any]] = {},
    ) -> "ClassWithClassmethodOverrides":
        return ClassWithClassmethodOverrides("overridden value", "json")

    @classmethod
    def from_bson(
        cls,
        document: dict[str, Any],
        custom_deserializers: dict[Type, Callable[[Any], Any]] = {},
    ) -> "ClassWithClassmethodOverrides":
        return ClassWithClassmethodOverrides("overridden value", "bson")

    @classmethod
    def as_mongodb_schema(
        cls,
        custom_handlers: dict[Type, Callable[[Any], Any]] = {},
    ) -> Any:
        return {"value": "overridden value", "format": "mongodb schema"}
