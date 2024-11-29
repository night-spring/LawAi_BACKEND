# Generated by Django 5.1.3 on 2024-11-26 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="IPC",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("section_id", models.TextField()),
                ("section_title", models.TextField()),
                ("description", models.TextField()),
            ],
        ),
    ]
