# Generated by Django 5.0.3 on 2024-03-08 09:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="reminder",
            name="sent",
            field=models.BooleanField(default=False),
        ),
    ]
