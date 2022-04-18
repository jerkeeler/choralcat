from django import template

register = template.Library()


@register.simple_tag
def get_elided_page_range(paginator, number, on_each_side=3, on_ends=2):
    return paginator.get_elided_page_range(number=number, on_each_side=on_each_side, on_ends=on_ends)


@register.inclusion_tag("web/catalog/search_attrs.txt")
def search_attrs(trigger: str = "click delay:100ms"):
    return {"trigger": trigger}
