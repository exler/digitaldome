# Generated by Django 5.1.4 on 2025-01-13 20:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("entities", "0009_alter_book_name_alter_game_name_alter_movie_name_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="book",
            options={"ordering": ("name", "-id")},
        ),
        migrations.AlterModelOptions(
            name="game",
            options={"ordering": ("name", "-id")},
        ),
        migrations.AlterModelOptions(
            name="movie",
            options={"ordering": ("name", "-id")},
        ),
        migrations.AlterModelOptions(
            name="show",
            options={"ordering": ("name", "-id")},
        ),
    ]
