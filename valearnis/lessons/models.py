from django.db import models
from django.utils.translation import gettext_lazy as _
from valearnis.users.models import User


# Create your models here.
class Lesson(models.Model):
    slug = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=128, blank=True, default="")
    description = models.TextField()
    img_url = models.TextField()


class LessonElement(models.Model):
    class LessonElementChoices(models.TextChoices):
        TEXT = "text", _("Text")
        IMAGE = "image", _("Image")

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    display_order = models.IntegerField()
    text = models.TextField()
    img_url = models.TextField()
    type = models.CharField(max_length=32, choices=LessonElementChoices.choices, default=LessonElementChoices.TEXT)


class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)


class Question(models.Model):
    class TypeChoices(models.TextChoices):
        SINGLE_MUTIPLE_CHOICE = "smc", _("Single Multiple Choice")
        MULTI_MULTIPLE_CHOICE = "mmc", _("Multi Multiple Choice")

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    type = models.CharField(max_length=32, choices=TypeChoices.choices, default=TypeChoices.SINGLE_MUTIPLE_CHOICE)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_answer = models.BooleanField(default=False)


class QuizAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    total_items = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=8, decimal_places=5, default=0)


class QuizAnswerItem(models.Model):
    quiz_answer = models.ForeignKey(QuizAnswer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Choice)
