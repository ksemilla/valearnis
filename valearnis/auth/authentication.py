from ninja.security import HttpBearer
from django.http import HttpRequest
from typing import Any
import jwt
from django.conf import settings
from valearnis.users.models import User


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Any | None:
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            request.user = User.objects.get(id=decoded["user_id"])
            return token
        except:
            return
