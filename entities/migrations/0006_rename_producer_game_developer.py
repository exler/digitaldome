# Generated by Django 4.2.6 on 2023-11-07 20:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("entities", "0005_book_goodreads_url_game_steam_url_movie_imdb_url_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="game",
            old_name="producer",
            new_name="developer",
        ),
    ]
