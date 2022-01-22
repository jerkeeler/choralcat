from django.db import models

from .consts import VARCHAR_LENGTH
from .utils import gen_token


class TimeStampMixin(object):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
            self.token = poss_token
        super(TokenModel, self).save(*args, **kwargs)


class CreatedByMixin(object):
    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        editable=False,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_creator_related",
        related_query_name="%(app_label)s_%(class)ss_creator",
    )
    updated_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        editable=False,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_updater_related",
        related_query_name="%(app_label)s_%(class)ss_updater",
    )


class StandardModel(TokenModel, TimeStampMixin):
    class Meta:
        abstract = True


class UserModel(StandardModel, CreatedByMixin):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        abstract = True
