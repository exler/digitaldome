# Generated by Django 4.2.6 on 2023-10-19 14:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("entities", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="show",
            name="created_by",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="show",
            name="creator",
            field=models.ManyToManyField(blank=True, related_name="created_shows", to="entities.identity"),
        ),
        migrations.AddField(
            model_name="show",
            name="stars",
            field=models.ManyToManyField(blank=True, related_name="starred_in_shows", to="entities.identity"),
        ),
        migrations.AddField(
            model_name="show",
            name="tags",
            field=models.ManyToManyField(blank=True, to="entities.tag"),
        ),
        migrations.AddField(
            model_name="movie",
            name="cast",
            field=models.ManyToManyField(blank=True, related_name="acted_in_movies", to="entities.identity"),
        ),
        migrations.AddField(
            model_name="movie",
            name="created_by",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="movie",
            name="director",
            field=models.ManyToManyField(blank=True, related_name="directed_movies", to="entities.identity"),
        ),
        migrations.AddField(
            model_name="movie",
            name="tags",
            field=models.ManyToManyField(blank=True, to="entities.tag"),
        ),
        migrations.AddField(
            model_name="identity",
            name="created_by",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="identity",
            name="tags",
            field=models.ManyToManyField(blank=True, to="entities.tag"),
        ),
        migrations.AddField(
            model_name="game",
            name="created_by",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="game",
            name="producer",
            field=models.ManyToManyField(blank=True, related_name="produced_games", to="entities.identity"),
        ),
        migrations.AddField(
            model_name="game",
            name="publisher",
            field=models.ManyToManyField(blank=True, related_name="published_games", to="entities.identity"),
        ),
        migrations.AddField(
            model_name="game",
            name="tags",
            field=models.ManyToManyField(blank=True, to="entities.tag"),
        ),
        migrations.AddField(
            model_name="book",
            name="author",
            field=models.ManyToManyField(blank=True, related_name="written_books", to="entities.identity"),
        ),
        migrations.AddField(
            model_name="book",
            name="created_by",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="tags",
            field=models.ManyToManyField(blank=True, to="entities.tag"),
        ),
    ]
