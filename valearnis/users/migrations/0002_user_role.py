# Generated by Django 4.2.5 on 2023-09-26 07:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(choices=[("user", "User"), ("admin", "Admin")], default="user", max_length=32),
        ),
    ]
