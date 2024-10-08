# Generated by Django 5.0.3 on 2024-06-11 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0028_rename_note_copy_copyid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowance",
            name="status",
            field=models.IntegerField(
                choices=[
                    (0, "request"),
                    (1, "rejected"),
                    (2, "borrowing"),
                    (3, "returned"),
                    (4, "overdue"),
                    (5, "lost"),
                ],
                default=0,
            ),
        ),
    ]
