from typing import Callable

from django.http import HttpRequest

from choralcat.web.types import CCHttpRequest


class OrganizationMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpRequest]) -> None:
        self.get_response = get_response

    def __call__(self, request: CCHttpRequest) -> HttpRequest:
        if request.user and request.user.is_authenticated:
            request.org = request.user.profile.organization

        return self.get_response(request)
