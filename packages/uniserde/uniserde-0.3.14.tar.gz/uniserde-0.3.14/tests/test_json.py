import base64
from datetime import datetime, timezone
from pathlib import Path

import models
import pytest

import uniserde


def test_serialize_exact_variant_1() -> None:
    value_fresh = models.TestClass.create_variant_1()
    value_json = value_fresh.as_json()

    assert value_json == {
        "valBool": value_fresh.val_bool,
        "valInt": value_fresh.val_int,
        "valFloat": value_fresh.val_float,
        "valBytes": base64.b64encode(value_fresh.val_bytes).decode("utf-8"),
        "valStr": value_fresh.val_str,
        "valDatetime": value_fresh.val_datetime.isoformat(),
        "valTimedelta": value_fresh.val_timedelta.total_seconds(),
        "valTuple": list(value_fresh.val_tuple),
        "valList": value_fresh.val_list,
        "valSet": list(value_fresh.val_set),
        "valDict": value_fresh.val_dict,
        "valOptional": value_fresh.val_optional,
        "valOldUnionOptional1": value_fresh.val_old_union_optional_1,
        "valOldUnionOptional2": value_fresh.val_old_union_optional_2,
        "valNewUnionOptional1": value_fresh.val_new_union_optional_1,
        "valNewUnionOptional2": value_fresh.val_new_union_optional_2,
        "valAny": value_fresh.val_any,
        "valObjectId": str(value_fresh.val_object_id),
        "valLiteral": value_fresh.val_literal,
        "valEnum": "one",
        "valFlag": ["one", "two"],
        "valPath": str(value_fresh.val_path),
    }


@pytest.mark.parametrize("lazy", [False, True])
def test_round_trip_variant_1(lazy: bool) -> None:
    value_fresh = models.TestClass.create_variant_1()
    value_json = value_fresh.as_json()
    value_round_trip = models.TestClass.from_json(value_json, lazy=lazy)

    assert value_fresh == value_round_trip


@pytest.mark.parametrize("lazy", [False, True])
def test_round_trip_variant_2(lazy: bool) -> None:
    value_fresh = models.TestClass.create_variant_2()
    value_json = value_fresh.as_json()
    value_round_trip = models.TestClass.from_json(value_json, lazy=lazy)

    assert value_fresh == value_round_trip


@pytest.mark.parametrize("lazy", [False, True])
def test_round_trip_parent(lazy: bool) -> None:
    value_fresh = models.ParentClass.create_parent_variant_1()
    value_json = value_fresh.as_json()
    value_round_trip = models.ParentClass.from_json(value_json, lazy=lazy)

    assert value_fresh == value_round_trip


@pytest.mark.parametrize("lazy", [False, True])
def test_round_trip_child(lazy: bool) -> None:
    value_fresh = models.ChildClass.create_child_variant_1()
    value_json = value_fresh.as_json()
    value_round_trip = models.ChildClass.from_json(value_json, lazy=lazy)

    assert value_fresh == value_round_trip


@pytest.mark.parametrize("lazy", [False, True])
def test_round_trip_child_as_parent(lazy: bool) -> None:
    value_fresh = models.ChildClass.create_child_variant_1()
    value_json = value_fresh.as_json()
    value_round_trip = models.ParentClass.from_json(value_json, lazy=lazy)

    assert isinstance(value_round_trip, models.ChildClass)
    assert value_fresh == value_round_trip


def test_kw_only() -> None:
    value_fresh = models.ClassWithKwOnly(1, bar=2)
    value_bson = value_fresh.as_bson()

    assert "foo" in value_bson
    assert "bar" in value_bson
    assert "_" not in value_bson
    assert len(value_bson) == 2
    assert value_bson["foo"] == 1
    assert value_bson["bar"] == 2


@pytest.mark.parametrize("lazy", [False, True])
def test_datetime_needs_timezone(lazy: bool) -> None:
    with pytest.raises(uniserde.SerdeError, match="is missing a timezone."):
        uniserde.from_json("2020-01-01T01:02:03.000004", datetime, lazy=lazy)


@pytest.mark.parametrize("lazy", [False, True])
def test_datetime_parses_timezone(lazy: bool) -> None:
    value_parsed = uniserde.from_json(
        "2020-01-01T01:02:03.000004Z",
        datetime,
        lazy=lazy,
    )

    assert isinstance(value_parsed, datetime)
    assert value_parsed.tzinfo is not None
    assert value_parsed == datetime(2020, 1, 1, 1, 2, 3, 4, timezone.utc)


@pytest.mark.parametrize("lazy", [False, True])
def test_int_is_float(lazy: bool) -> None:
    uniserde.from_json(1, float, lazy=lazy)


@pytest.mark.parametrize("lazy", [False, True])
def test_paths_are_made_absolute(lazy: bool) -> None:
    path_relative = Path.home() / "folder"
    path_relative = path_relative.relative_to(Path.home())
    assert not path_relative.is_absolute()

    path_absolute = path_relative.absolute()
    assert path_absolute.is_absolute()

    path_serialized = uniserde.as_json(path_relative)
    assert path_serialized == str(path_absolute)

    path_deserialized = uniserde.from_json(path_serialized, Path, lazy=lazy)
    assert path_deserialized == path_absolute


def test_catch_superfluous_value() -> None:
    with pytest.raises(uniserde.SerdeError, match="Superfluous object field"):
        uniserde.from_json(
            {
                "foo": 1,
                "bar": "one",
                "invalidKey": True,
            },
            models.SimpleClass,
        )


def test_overridden_as_json() -> None:
    value_fresh = models.ClassWithStaticmethodOverrides.create()
    value_json = uniserde.as_json(value_fresh)

    assert value_json == {
        "value": "overridden value",
        "format": "json",
    }


@pytest.mark.parametrize("lazy", [False, True])
def test_overridden_from_json_staticmethod(lazy: bool) -> None:
    value_json = {
        "value": "actual value",
        "format": "json",
    }
    value_parsed = uniserde.from_json(
        value_json,
        models.ClassWithStaticmethodOverrides,
        lazy=lazy,
    )

    assert isinstance(value_parsed, models.ClassWithStaticmethodOverrides)
    assert value_parsed.value == "overridden value"
    assert value_parsed.format == "json"


@pytest.mark.parametrize("lazy", [False, True])
def test_overridden_from_json_classmethod(lazy: bool) -> None:
    value_json = {
        "value": "actual value",
        "format": "json",
    }
    value_parsed = uniserde.from_json(
        value_json,
        models.ClassWithClassmethodOverrides,
        lazy=lazy,
    )

    assert isinstance(value_parsed, models.ClassWithClassmethodOverrides)
    assert value_parsed.value == "overridden value"
    assert value_parsed.format == "json"
