import logging

from django.db import models

from .consts import VARCHAR_LENGTH
from .utils import gen_token

logger = logging.getLogger(__name__)


class TimeStampMixin(object):
    class Meta:
        abstract = True


class CreatedByMixin(object):
    class Meta:
        abstract = True


class TokenModel(models.Model):
    token = models.CharField(
        max_length=VARCHAR_LENGTH,
        editable=True,
        blank=True,
        unique=True,
        null=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.token:
            poss_token = gen_token()
            while len(type(self).objects.filter(token=poss_token)) > 0:
                poss_token = gen_token()
            logger.debug(
                f"Created new token {poss_token} for model {self.__class__.__name__}"
            )
            self.token = poss_token
        super(TokenModel, self).save(*args, **kwargs)


class UserModel(TokenModel):
    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_creator_related",
        related_query_name="%(app_label)s_%(class)ss_creator",
    )
    updated_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_updater_related",
        related_query_name="%(app_label)s_%(class)ss_updater",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        abstract = True
