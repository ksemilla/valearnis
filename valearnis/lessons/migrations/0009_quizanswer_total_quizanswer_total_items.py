# Generated by Django 4.2.5 on 2023-09-28 22:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0008_quizansweritem_quiz_answer"),
    ]

    operations = [
        migrations.AddField(
            model_name="quizanswer",
            name="total",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="quizanswer",
            name="total_items",
            field=models.IntegerField(default=0),
        ),
    ]
