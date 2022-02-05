import hashlib

from django import template

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


@register.inclusion_tag("web/tag.html")
def create_tag(tag: str):
    return _get_tag_info(tag)


@register.inclusion_tag("web/tag_with_remove.html")
def create_closeable_tag(tag: str, tag_url: str, widget_name: str):
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


@register.simple_tag
def get_elided_page_range(paginator, number, on_each_side=3, on_ends=2):
    return paginator.get_elided_page_range(
        number=number, on_each_side=on_each_side, on_ends=on_ends
    )
