import warnings
from typing import *  # type: ignore

import models
import pytest

import uniserde

# This throws a warning since 3.11, which shows up rather confusingly in pytest.
# Suppress it. (The warning is caused by `mongo_schema`, not uniserde.)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import mongo_schema

try:
    import bson  # type: ignore
except ImportError:
    bson = None


@pytest.mark.skipif(bson is None, reason="`pymongo` is not installed")
@pytest.mark.parametrize(
    "value,value_type",
    [
        (models.TestClass.create_variant_1(), models.TestClass),
        (models.TestClass.create_variant_2(), models.TestClass),
        (models.ParentClass.create_parent_variant_1(), models.ParentClass),
        (models.ChildClass.create_child_variant_1(), models.ChildClass),
        (models.ChildClass.create_child_variant_1(), models.ParentClass),
        (models.ClassWithId.create(), models.ClassWithId),
        (models.ClassWithKwOnly.create(), models.ClassWithKwOnly),
    ],
)
def test_value_matches_schema(
    value: uniserde.Serde,
    value_type: Type[uniserde.Serde],
) -> None:
    schema = uniserde.as_mongodb_schema(value_type)
    bson_value = value.as_bson()

    mongo_schema.validate(bson_value, schema)


def test_overridden_as_mongodb_schema_staticmethod() -> None:
    value_schema = uniserde.as_mongodb_schema(models.ClassWithStaticmethodOverrides)

    assert value_schema == {
        "value": "overridden value",
        "format": "mongodb schema",
    }


def test_overridden_as_mongodb_schema_classmethod() -> None:
    value_schema = uniserde.as_mongodb_schema(models.ClassWithClassmethodOverrides)

    assert value_schema == {
        "value": "overridden value",
        "format": "mongodb schema",
    }
