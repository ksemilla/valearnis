from ninja import NinjaAPI

# from royalties.auth.auth_interface import AuthBearer

# from royalties.contracts.views import contracts_router, clients_router

from valearnis.users.views import user_router
from valearnis.auth.views import auth_router
from valearnis.lessons.views import lessons_router, quizz_answers_router


api = NinjaAPI()

api.add_router("users/", user_router)
api.add_router("auth/", auth_router)
api.add_router("lessons/", lessons_router)
api.add_router("quiz-answers/", quizz_answers_router)


class InvalidToken(Exception):
    pass


@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)


@api.exception_handler(PermissionError)
def on_permission_denied(request, exc):
    return api.create_response(request, {"detail": "Permission denied"}, status=403)
