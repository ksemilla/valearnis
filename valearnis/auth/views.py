from ninja import Router
from .schema import LoginSchema, AccessToken
from valearnis.users.models import User
from valearnis.utils.schema import Error
import jwt
from django.conf import settings
from valearnis.users.schema import UserSchema

auth_router = Router()


@auth_router.post("", response={200: AccessToken, 400: Error})
def login(request, data: LoginSchema):
    user = User.objects.filter(email=data.email).first()

    if not user:
        return 400, {"detail": "User not found"}

    correct_password = user.check_password(data.password)
    if not correct_password:
        return 400, {"detail": "Incorrect password"}

    encoded_jwt = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")

    return {"access_token": encoded_jwt}


@auth_router.post("verify/", response={200: UserSchema, 400: Error})
def verify_token(request, data: AccessToken):
    try:
        decoded = jwt.decode(data.access_token, settings.SECRET_KEY, algorithms="HS256")

        user = User.objects.filter(id=decoded["user_id"]).first()

        return user

    except:
        return 400, {"detail": "Invalid token"}
