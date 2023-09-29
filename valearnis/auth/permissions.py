import functools
from django.http import HttpRequest
from valearnis.users.models import User


def permission_decorator(*perms):
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # You can access the passed argument 'arg' here
            for perm in perms:
                perm.verify(request, *args, **kwargs)
            # BEFORE RESULT
            result = view_func(request, *args, **kwargs)
            # AFTER RESULT
            return result

        return wrapper

    return decorator


class BasePermission:
    @classmethod
    def verify(cls, request: HttpRequest, *args, **kwargs):
        if not cls.has_perm(request, *args, **kwargs):
            raise PermissionError

    @classmethod
    def has_perm(cls, request, *args, **kwargs):
        raise NotImplementedError


class IsAdmin(BasePermission):
    @classmethod
    def has_perm(cls, request: HttpRequest, *args, **kwargs):
        return request.user.role == User.RoleChoices.ADMIN.value


class IsOwner(BasePermission):
    pass
    # @classmethod
    # def has_perm(cls, request: HttpRequest, *args, **kwargs):
    #     return True
