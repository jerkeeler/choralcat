import hashlib
import os
from glob import glob

from django import template
from django.conf import settings

register = template.Library()

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
def tag(tag: str):
    return _get_tag_info(tag)


@register.inclusion_tag("web/components/tag_with_remove.html")
def closeable_tag(tag: str, tag_url: str, widget_name: str):
    tag_info = _get_tag_info(tag)
    tag_info["tag_url"] = tag_url
    tag_info["widget_name"] = widget_name
    return tag_info


def _get_tag_info(tag: str):
    color = _get_color(tag)
    return {
        "tag": tag,
        "bg_class": color[0],
        "text_class": color[1],
    }


def _create_icon_component(name: str):
    @register.inclusion_tag(f"web/components/icons/{name}.html", name=f"{name}_icon")
    def _icon(classes: str = ""):
        return {"classes": classes}


# Dynamically create all icon tags from html files
icon_glob = os.path.join(settings.BASE_DIR, "choralcat", "web", "templates", "web", "components", "icons", "*.html")
for icon in glob(icon_glob):
    icon_name = os.path.splitext(os.path.basename(icon))[0]
    _create_icon_component(icon_name)


@register.inclusion_tag("web/components/buttons/button_link.html")
def button_link(location: str, text: str):
    return {"location": location, "text": text}
