from operator import itemgetter
from typing import Any

from django.forms.widgets import SelectMultiple


class TagWidget(SelectMultiple):
    template_name = "partials/forms/tag_widget.html"

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
