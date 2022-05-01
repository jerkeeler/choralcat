import logging
from typing import Any, Type

from django.db.models import Model, QuerySet
from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import BaseFormView, ModelFormMixin

from choralcat.core.views import UserCreateView, UserUpdateView
from choralcat.web.query import org_filter
from choralcat.web.types import CCHttpRequest

logger = logging.getLogger(__name__)


class OrgFormMixin(TemplateResponseMixin, ModelFormMixin, BaseFormView):
    request: CCHttpRequest

    def form_valid(self, form: Any) -> HttpResponse:
        logger.info(
            f"{form.instance.__class__.__name__} {form.instance} created by "
            f"{self.request.user} for org {self.request.org}"
        )
        form.instance.organization = self.request.org
        return super().form_valid(form)

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["org"] = self.request.org
        return kwargs


class OrgCreateView(OrgFormMixin, UserCreateView):
    pass


class OrgUpdateView(OrgFormMixin, UserUpdateView):
    pass


class OrgFilterMixin(TemplateResponseMixin, View):
    model: Type[Model]
    request: CCHttpRequest

    def get_queryset(self) -> QuerySet[Model]:
        return org_filter(self.model, self.request)
