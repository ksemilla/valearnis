# Generated by Django 4.2.5 on 2023-09-28 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0007_remove_question_answers"),
    ]

    operations = [
        migrations.AddField(
            model_name="quizansweritem",
            name="quiz_answer",
            field=models.ForeignKey(default="", on_delete=django.db.models.deletion.CASCADE, to="lessons.quizanswer"),
            preserve_default=False,
        ),
    ]
