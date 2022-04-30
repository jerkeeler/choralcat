import logging
from typing import Any

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .consts import DEFAULT_TIME_ZONE
from .models import Organization, UserProfile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_user_profile")
def create_user_profile(instance: User, created: bool, **_: Any) -> None:
    logger.debug("Signal for user post-save")
    if created and not UserProfile.objects.filter(user=instance).exists():
        # For now automatically add everyone to the chanticleer organization, should be updated if choralcat
        # ever moves beyond chanticleer.
        chanticleer = Organization.objects.get(name="Chanticleer")
        UserProfile.objects.create(user=instance, timezone=DEFAULT_TIME_ZONE, organization=chanticleer)
        logger.info(
            f"Created new user profile object for {instance.username} with default "
            f"timezone {DEFAULT_TIME_ZONE} and organization {chanticleer}"
        )
