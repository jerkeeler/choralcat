from operator import itemgetter
from typing import Any, Type

from django.db import models
from django.forms.widgets import SelectMultiple, TextInput


class TagWidget(SelectMultiple):
    template_name = "web/widgets/tag_widget.html"

    def get_context(self, name: str, value: Any, attrs):
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

    def __init__(self, model: Type[models.Model], field: str, attrs=None):
        super().__init__(attrs)
        self.model = model
        self.field = field

    def get_context(self, name: str, value: Any, attrs):
        context = super().get_context(name, value, attrs)
        ordered_opts = [
            o for o in sorted(self.model.objects.order_by().values_list(self.field, flat=True).distinct()) if o
        ]
        context["ordered_options"] = ordered_opts
        return context


class MtMStringWidget(TagWidget):
    template_name = "web/widgets/mtm_widget.html"
