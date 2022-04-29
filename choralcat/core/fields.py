import logging
from typing import Any, Optional, Union

from django.db import models
from django.db.models.manager import BaseManager
from unidecode import unidecode

from .utils import gen_slug

logger = logging.getLogger(__name__)


class AutoSlugField(models.SlugField):
    description = "A field that autogenerates a unique slug based on another field"
    manager: BaseManager[models.Model]

    def __init__(self, populated_from: Optional[Union[str, list[str]]] = None, *args: Any, **kwargs: Any) -> None:
        if populated_from is None:
            raise ValueError("populated_from has to be provided")
        self.populated_from = populated_from

        if "null" not in kwargs:
            kwargs["null"] = True

        if "blank" not in kwargs:
            kwargs["blank"] = True

        if "unique" not in kwargs:
            kwargs["unique"] = True

        if "db_index" not in kwargs:
            kwargs["db_index"] = True

        super().__init__(*args, **kwargs)

    def deconstruct(self) -> tuple[str, str, Any, Any]:
        name, path, args, kwargs = super().deconstruct()
        if self.populated_from is not None:
            kwargs["populated_from"] = self.populated_from
        return name, path, args, kwargs

    def pre_save(self, model_instance: models.Model, add: bool) -> Any:
        value = self.value_from_object(model_instance)

        if value:
            return value

        if hasattr(self, "manager") and self.manager is not None:
            manager = self.manager
        else:
            manager = self.model._default_manager

        if self.populated_from is not None and type(self.populated_from) is str:
            attr_value = getattr(model_instance, self.populated_from)
        elif self.populated_from is not None and type(self.populated_from) is list:
            attr_value = " ".join(getattr(model_instance, f) for f in self.populated_from)
        else:
            attr_value = ""

        # NOTE: There is a slight race condition here where another object is saved with the same slug just after the
        # filter. However, given in this instance we are appending a random token to the end of the slug the chances
        # are very very slim at the moment.
        while True:
            slug = gen_slug(attr_value)
            others = manager.filter(**{self.name: slug})
            if not others:
                # make the updated slug available as instance attribute
                setattr(model_instance, self.name, slug)
                logger.debug(f"Generated new slug for field {self.name}: {slug}")
                return slug


class UnidecodeField(models.CharField):
    description = "A field that automatically unidecodes another field upon each save"

    def __init__(self, populated_from: Optional[str] = None, *args: Any, **kwargs: Any) -> None:
        if populated_from is None:
            raise ValueError("populated_from has to be provided")
        self.populated_from = populated_from

        if "null" not in kwargs:
            kwargs["null"] = True

        if "blank" not in kwargs:
            kwargs["blank"] = True

        super().__init__(*args, **kwargs)

    def deconstruct(self) -> tuple[str, str, Any, Any]:
        name, path, args, kwargs = super().deconstruct()
        if self.populated_from is not None:
            kwargs["populated_from"] = self.populated_from
        return name, path, args, kwargs

    def pre_save(self, model_instance: models.Model, add: bool) -> str:
        attr_value = getattr(model_instance, self.populated_from)
        return unidecode(attr_value)
