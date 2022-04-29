from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag
def get_elided_page_range(paginator: Paginator, number: int, on_each_side: int = 3, on_ends: int = 2) -> int:
    return paginator.get_elided_page_range(number=number, on_each_side=on_each_side, on_ends=on_ends)  # type: ignore


@register.inclusion_tag("web/catalog/search_attrs.txt")
def search_attrs(trigger: str = "click delay:100ms") -> dict[str, str]:
    return {"trigger": trigger}
