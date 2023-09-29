from django.contrib import admin
from .models import LessonElement, Lesson, QuizAnswer, QuizAnswerItem

admin.site.register(LessonElement)
admin.site.register(Lesson)
admin.site.register(QuizAnswer)
admin.site.register(QuizAnswerItem)
