from datetime import datetime, timezone

import models
import pytest

import uniserde


def test_serialize_exact_variant_1() -> None:
    value_fresh = models.TestClass.create_variant_1()
    value_bson = value_fresh.as_bson()

    print(value_bson)

    assert value_bson == {
        "valBool": value_fresh.val_bool,
        "valInt": value_fresh.val_int,
        "valFloat": value_fresh.val_float,
        "valBytes": value_fresh.val_bytes,
        "valStr": value_fresh.val_str,
        "valDatetime": value_fresh.val_datetime,
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
        "valObjectId": value_fresh.val_object_id,
        "valLiteral": value_fresh.val_literal,
        "valEnum": "one",
        "valFlag": ["one", "two"],
        "valPath": str(value_fresh.val_path),
    }


@pytest.mark.parametrize("lazy", [False, True])
def test_round_trip_variant_1(lazy: bool) -> None:
    value_fresh = models.TestClass.create_variant_1()
    value_bson = value_fresh.as_bson()
    value_round_trip = models.TestClass.from_bson(value_bson, lazy=lazy)

    assert value_fresh == value_round_trip


@pytest.mark.parametrize("lazy", [False, True])
def test_round_trip_variant_2(lazy: bool) -> None:
    value_fresh = models.TestClass.create_variant_2()
    value_bson = value_fresh.as_bson()
    value_round_trip = models.TestClass.from_bson(value_bson, lazy=lazy)

    assert value_fresh == value_round_trip


@pytest.mark.parametrize("lazy", [False, True])
def test_round_trip_parent(lazy: bool) -> None:
    value_fresh = models.ParentClass.create_parent_variant_1()
    value_bson = value_fresh.as_bson()
    value_round_trip = models.ParentClass.from_bson(value_bson, lazy=lazy)

    assert value_fresh == value_round_trip


@pytest.mark.parametrize("lazy", [False, True])
def test_round_trip_child(lazy: bool) -> None:
    value_fresh = models.ChildClass.create_child_variant_1()
    value_bson = value_fresh.as_bson()
    value_round_trip = models.ChildClass.from_bson(value_bson, lazy=lazy)

    assert value_fresh == value_round_trip


@pytest.mark.parametrize("lazy", [False, True])
def test_round_trip_child_as_parent(lazy: bool) -> None:
    value_fresh = models.ChildClass.create_child_variant_1()
    value_bson = value_fresh.as_bson()
    value_round_trip = models.ParentClass.from_bson(value_bson, lazy=lazy)

    assert isinstance(value_round_trip, models.ChildClass)
    assert value_fresh == value_round_trip


def test_rename_id() -> None:
    value_fresh = models.ClassWithId(1, 2)
    value_bson = value_fresh.as_bson()

    assert "_id" in value_bson
    assert "id" not in value_bson
    assert "foo" in value_bson
    assert len(value_bson) == 2


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
def test_datetime_imputes_timezone(lazy: bool) -> None:
    # MongoDB does not explicitly store timezone information, but rather
    # converts everything to UTC. Make sure uniserde understands this and
    # imputes UTC.
    value_parsed = uniserde.from_bson(
        datetime(2020, 1, 1, 1, 2, 3, 4),
        datetime,
        lazy=lazy,
    )

    assert isinstance(value_parsed, datetime)
    assert value_parsed.tzinfo is not None
    assert value_parsed == datetime(2020, 1, 1, 1, 2, 3, 4, timezone.utc)


def test_int_is_float() -> None:
    uniserde.from_bson(1, float)


def test_catch_superfluous_value() -> None:
    with pytest.raises(uniserde.SerdeError, match="Superfluous object field"):
        uniserde.from_bson(
            {
                "foo": 1,
                "bar": "one",
                "invalidKey": True,
            },
            models.SimpleClass,
        )


def test_overridden_as_bson() -> None:
    value_fresh = models.ClassWithStaticmethodOverrides.create()
    value_bson = uniserde.as_bson(value_fresh)

    assert value_bson == {
        "value": "overridden value",
        "format": "bson",
    }


@pytest.mark.parametrize("lazy", [False, True])
def test_overridden_from_bson_staticmethod(lazy: bool) -> None:
    value_bson = {
        "value": "actual value",
        "format": "bson",
    }
    value_parsed = uniserde.from_bson(
        value_bson,
        models.ClassWithStaticmethodOverrides,
        lazy=lazy,
    )

    assert isinstance(value_parsed, models.ClassWithStaticmethodOverrides)
    assert value_parsed.value == "overridden value"
    assert value_parsed.format == "bson"


@pytest.mark.parametrize("lazy", [False, True])
def test_overridden_from_bson_classmethod(lazy: bool) -> None:
    value_bson = {
        "value": "actual value",
        "format": "bson",
    }
    value_parsed = uniserde.from_bson(
        value_bson,
        models.ClassWithClassmethodOverrides,
        lazy=lazy,
    )

    assert isinstance(value_parsed, models.ClassWithClassmethodOverrides)
    assert value_parsed.value == "overridden value"
    assert value_parsed.format == "bson"
