import zoneinfo

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.user and request.user.is_authenticated:
                user_timezone = request.user.profile.timezone
                timezone.activate(zoneinfo.ZoneInfo(user_timezone))
        except (ObjectDoesNotExist, zoneinfo.ZoneInfoNotFoundError):
            print(f"No user profile or invalid timezone for user {str(request.user)}")
            timezone.deactivate()

        return self.get_response(request)
