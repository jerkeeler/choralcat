import dataclasses
from typing import Any


def camel_to_snake(input_str: str) -> str:
    return "".join("_" + c.lower() if c.isupper() else c for c in input_str).lstrip("_")


def assert_field_instance(instance: Any, field: dataclasses.Field) -> None:
    assert isinstance(instance, field.type), f"{field.name} expected type {field.type} but found {type(instance)}"
