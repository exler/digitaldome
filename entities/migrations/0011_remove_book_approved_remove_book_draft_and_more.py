# Generated by Django 5.1.5 on 2025-01-22 21:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("entities", "0010_alter_book_options_alter_game_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="book",
            name="draft",
        ),
        migrations.RemoveField(
            model_name="game",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="game",
            name="draft",
        ),
        migrations.RemoveField(
            model_name="movie",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="movie",
            name="draft",
        ),
        migrations.RemoveField(
            model_name="show",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="show",
            name="draft",
        ),
    ]