import models
import pytest

import uniserde.lazy_wrapper


def test_missing_attribute_raises_attribute_error() -> None:
    # Create a non-lazy instance
    value_eager = models.TestClass.create_variant_1()

    # Create a lazy instance of the same class
    value_lazy = models.TestClass.from_json(value_eager.as_json(), lazy=True)

    assert type(value_eager).__getattr__ is uniserde.lazy_wrapper._lazy_getattr  # type: ignore

    # This has modified the class' `__getattr__` method. Now test that accessing
    # an invalid attribute in fact raises an `AttributeError`, rather than just
    # failing, e.g. because the class is missing some fields expected to be
    # contained in lazy instances.
    with pytest.raises(AttributeError):
        value_eager.this_is_an_invalid_attribute_name  # type: ignore
