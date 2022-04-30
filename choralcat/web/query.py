from typing import Any, Type, TypeVar

from django.db import models
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404 as _old_get_object_or_404

from choralcat.web.types import CCHttpRequest

T = TypeVar("T", bound=models.Model)


def org_filter(model: Type[T], request: CCHttpRequest) -> QuerySet[T]:
    return model.objects.filter(organization=request.org)


def get_object_or_404(klass: Type[T], request: CCHttpRequest, *args: Any, **kwargs: Any) -> T:
    return _old_get_object_or_404(klass, organization=request.org, *args, **kwargs)
