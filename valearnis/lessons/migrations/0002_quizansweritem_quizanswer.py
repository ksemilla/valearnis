# Generated by Django 4.2.5 on 2023-09-26 00:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("lessons", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuizAnswerItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("answers", models.ManyToManyField(to="lessons.choice")),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lessons.question")),
            ],
        ),
        migrations.CreateModel(
            name="QuizAnswer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quiz", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lessons.quiz")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
