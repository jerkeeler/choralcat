from typing import Optional

from django.contrib.auth.models import User
from django.http import HttpRequest

from choralcat.web.models import Organization, UserProfile


class CCUser(User):
    profile: UserProfile


class CCHttpRequest(HttpRequest):
    user: CCUser
    org: Optional[Organization]
