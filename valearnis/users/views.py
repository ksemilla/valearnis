# from django.contrib.auth import get_user_model
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.messages.views import SuccessMessageMixin
# from django.urls import reverse
# from django.utils.translation import gettext_lazy as _
# from django.views.generic import DetailView, RedirectView, UpdateView

# User = get_user_model()


# class UserDetailView(LoginRequiredMixin, DetailView):
#     model = User
#     slug_field = "id"
#     slug_url_kwarg = "id"


# user_detail_view = UserDetailView.as_view()


# class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = User
#     fields = ["name"]
#     success_message = _("Information successfully updated")

#     def get_success_url(self):
#         assert self.request.user.is_authenticated  # for mypy to know that the user is authenticated
#         return self.request.user.get_absolute_url()

#     def get_object(self):
#         return self.request.user


# user_update_view = UserUpdateView.as_view()


# class UserRedirectView(LoginRequiredMixin, RedirectView):
#     permanent = False

#     def get_redirect_url(self):
#         return reverse("users:detail", kwargs={"pk": self.request.user.pk})


# user_redirect_view = UserRedirectView.as_view()

from ninja import Router
from .schema import CreateUserSchema, UserSchema, UserUpdateSchema, StatsSchema
from .models import User
from typing import List
import jwt
from django.conf import settings
from valearnis.auth.schema import AccessToken
from valearnis.utils.schema import Error
from valearnis.lessons.models import QuizAnswer
from valearnis.lessons.schema import QuizAnswerListSchema
from django.db.models import Sum, Avg
from valearnis.auth.authentication import AuthBearer

user_router = Router()


@user_router.get("", response={200: List[UserSchema]}, auth=AuthBearer())
def get_users(request):
    return User.objects.all()


@user_router.post("", response={200: AccessToken})
def create_user(request, data: CreateUserSchema):
    user = User.objects.create(email=data.email)
    user.set_password(data.password)
    user.save()

    encoded_jwt = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")

    return {"access_token": encoded_jwt}


@user_router.get("{id}/", response={200: UserSchema, 400: Error}, auth=AuthBearer())
def get_user(request, id: int):
    user = User.objects.filter(id=id).first()
    if not user:
        return 400, {"detail": "User not found"}
    return user


@user_router.put("{id}/", response={200: UserSchema, 400: Error}, auth=AuthBearer())
def get_user(request, id: int, data: UserUpdateSchema):
    user = User.objects.filter(id=id).first()
    if not user:
        return 400, {"detail": "User not found"}

    for field, value in data.dict().items():
        setattr(user, field, value)
    user.save()

    return user


@user_router.get("{id}/stats/", response={200: StatsSchema, 400: Error}, auth=AuthBearer())
def get_user(request, id: int):
    user = User.objects.filter(id=id).first()
    if not user:
        return 400, {"detail": "User not found"}
    qa = user.quizanswer_set.all()
    total_and_average = QuizAnswer.objects.filter(user__id=user.id).aggregate(
        total=Sum("total"), average=Avg("percentage")
    )

    stats = StatsSchema(
        total_quizzes=qa.count(),
        average_percentage=float(total_and_average["average"] if total_and_average["average"] else 0),
    )

    return stats


@user_router.get("{id}/quiz-answers/", response={200: List[QuizAnswerListSchema]}, auth=AuthBearer())
def get_quizzes(request):
    return QuizAnswer.objects.filter(user__id=request.user.id)
