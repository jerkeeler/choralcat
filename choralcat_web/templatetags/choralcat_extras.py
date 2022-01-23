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


@register.inclusion_tag("partials/tag.html")
def create_tag(tag):
    color = abs(hash(tag)) % len(tag_colors)
    return {
        "tag": tag,
        "bg_class": tag_colors[color][0],
        "text_class": tag_colors[color][1],
    }
