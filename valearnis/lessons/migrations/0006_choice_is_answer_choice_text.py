# Generated by Django 4.2.5 on 2023-09-27 06:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0005_lesson_img_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="choice",
            name="is_answer",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="choice",
            name="text",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
