from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, TextChoices
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from valearnis.users.managers import UserManager


class User(AbstractUser):
    class RoleChoices(TextChoices):
        USER = "user", _("User")
        ADMIN = "admin", _("Admin")

    """
    Default custom user model for valearnis.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    role = CharField(max_length=32, choices=RoleChoices.choices, default=RoleChoices.USER)

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
