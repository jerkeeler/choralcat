import dataclasses
import hashlib
import os
from glob import glob
from typing import Any, Callable, Optional, Type, TypeVar

from django import template
from django.conf import settings
from django.forms.boundfield import BoundField

from choralcat.web.utils import assert_field_instance, camel_to_snake

register = template.Library()
COMPONENTS_DIR = os.path.join("web", "components")

tag_colors = [
    ("bg-yellow-100", "text-yellow-800"),
    ("bg-red-100", "text-red-800"),
    ("bg-green-100", "text-green-800"),
    ("bg-sky-100", "text-sky-800"),
    ("bg-violet-100", "text-violet-800"),
    ("bg-stone-100", "text-stone-800"),
    ("bg-orange-100", "text-orange-800"),
]


def _consistent_hash(input_str: str) -> str:
    return hashlib.md5(input_str.encode("utf-8")).hexdigest()


def _get_color(input_str: str) -> tuple[str, str]:
    return tag_colors[int(_consistent_hash(input_str), 16) % len(tag_colors)]


@register.inclusion_tag("web/components/tag.html")
def tag(tag: str) -> dict[str, str]:
    return _get_tag_info(tag)


@register.inclusion_tag("web/components/tag_with_remove.html")
def closeable_tag(tag: str, tag_url: str, widget_name: str) -> dict[str, str]:
    tag_info = _get_tag_info(tag)
    tag_info["tag_url"] = tag_url
    tag_info["widget_name"] = widget_name
    return tag_info


def _get_tag_info(tag: str) -> dict[str, str]:
    color = _get_color(tag)
    return {
        "tag": tag,
        "bg_class": color[0],
        "text_class": color[1],
    }


def _create_icon_component(name: str) -> None:
    @register.inclusion_tag(f"web/components/icons/{name}.html", name=f"{name}_icon")
    def _icon(classes: str = "") -> dict[str, str]:
        return {"classes": classes}


# Dynamically create all icon tags from html files
icon_glob = os.path.join(settings.BASE_DIR, "choralcat", "web", "templates", "web", "components", "icons", "*.html")
for icon in glob(icon_glob):
    icon_name = os.path.splitext(os.path.basename(icon))[0]
    _create_icon_component(icon_name)


T = TypeVar("T")


def component(template_str: Optional[str] = None) -> Callable[[Type[T]], Type[T]]:
    def wrapper(component_class: Type[T]) -> Type[T]:
        cls = dataclasses.dataclass(component_class)
        fields = dataclasses.fields(cls)
        field_dct = {field.name: field for field in fields}
        component_name = camel_to_snake(cls.__name__)
        template_name = f"{template_str}.html" if template_str else f"{component_name}.html"

        @register.inclusion_tag(os.path.join(COMPONENTS_DIR, template_name), name=component_name)
        def _(*args: Any, **kwargs: Any) -> dict:
            res = {}
            for kwarg_key, kwarg_value in kwargs.items():
                assert kwarg_key in field_dct, f"kwarg {kwarg_key} is not valid for component {component_name}"
                field = field_dct[kwarg_key]
                assert_field_instance(kwarg_value, field)
                res[field.name] = kwarg_value
            for field, arg in zip(fields, args):
                assert_field_instance(arg, field)
                res[field.name] = arg
            return res

        return cls

    return wrapper


@component("buttons/button")
class Button:
    type: str
    text: str


@component("buttons/button_link")
class ButtonLink:
    location: str
    text: str


@component("forms/action_button")
class FormActionButton:
    label: str


@component("forms/cancel_button")
class FormCancelButton:
    label: str
    url: str


@component("forms/text_input")
class TextInput:
    field: BoundField
    label: str


@component("forms/tag_input")
class TagInput:
    field: BoundField
    label: str


@component("forms/checkbox")
class Checkbox:
    field: BoundField
    label: str


@component()
class TableHeaderWithAction:
    text: str
    location: str
    action_text: str
