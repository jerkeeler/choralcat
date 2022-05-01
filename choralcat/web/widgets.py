from operator import itemgetter
from typing import Any, Optional

from django.db import models
from django.db.models import QuerySet
from django.forms.widgets import SelectMultiple, TextInput


class TagWidget(SelectMultiple):
    template_name = "web/widgets/tag_widget.html"
    queryset: Optional[QuerySet[models.Model]]

    def __init__(self, attrs: Optional[dict[str, Any]] = None) -> None:
        super().__init__(attrs)
        self.queryset = None

    def get_context(self, name: str, value: str, attrs: Optional[dict[str, Any]]) -> dict[str, Any]:
        context = super().get_context(name, value, attrs)
        context["widget_name"] = context["widget"]["name"]
        context["selected"] = [
            {
                "label": opt[1][0]["label"],
                "value": opt[1][0]["value"],
            }
            for opt in context["widget"]["optgroups"]
            if opt[1][0]["selected"]
        ]
        context["sorted_options"] = sorted(
            [
                {
                    "label": opt[1][0]["label"],
                    "value": opt[1][0]["value"],
                }
                for opt in context["widget"]["optgroups"]
            ],
            key=itemgetter("label"),
        )
        return context


class AutocompleteStringWidget(TextInput):
    template_name = "web/widgets/string_widget.html"
    queryset: Optional[QuerySet[models.Model]]

    def __init__(self, field: str, attrs: Optional[dict[str, Any]] = None) -> None:
        super().__init__(attrs)
        self.field = field
        self.queryset = None

    def get_context(self, name: str, value: Any, attrs: Optional[dict[str, Any]]) -> dict[str, Any]:
        context = super().get_context(name, value, attrs)
        ordered_opts = []
        if self.queryset:
            ordered_opts = [
                o for o in sorted(self.queryset.order_by().values_list(self.field, flat=True).distinct()) if o
            ]
        context["ordered_options"] = ordered_opts
        return context


class MtMStringWidget(TagWidget):
    template_name = "web/widgets/mtm_widget.html"
