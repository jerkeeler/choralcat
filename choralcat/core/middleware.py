import logging
import zoneinfo

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

logger = logging.getLogger(__name__)


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.user and request.user.is_authenticated:
                user_timezone = request.user.profile.timezone
                logger.debug(f"Setting user {request.user} timezone to {user_timezone}")
                timezone.activate(zoneinfo.ZoneInfo(user_timezone))
        except (ObjectDoesNotExist, zoneinfo.ZoneInfoNotFoundError):
            logger.error(f"No user profile or invalid timezone for user {request.user}")
            timezone.deactivate()

        return self.get_response(request)
