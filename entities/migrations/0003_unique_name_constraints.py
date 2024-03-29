# Generated by Django 4.2.6 on 2023-10-19 17:19

import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("entities", "0002_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="book",
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower("name"), name="book_unique_name"),
        ),
        migrations.AddConstraint(
            model_name="game",
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower("name"), name="game_unique_name"),
        ),
        migrations.AddConstraint(
            model_name="identity",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("name"), name="identity_unique_name"
            ),
        ),
        migrations.AddConstraint(
            model_name="movie",
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower("name"), name="movie_unique_name"),
        ),
        migrations.AddConstraint(
            model_name="show",
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower("name"), name="show_unique_name"),
        ),
    ]
