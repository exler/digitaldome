# Generated by Django 5.2 on 2025-04-27 17:17

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("entities", "0020_alter_book_slug_alter_game_slug_alter_movie_slug_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="booktag",
            name="aliases",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255), blank=True, default=list, size=None
            ),
        ),
        migrations.AddField(
            model_name="gametag",
            name="aliases",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255), blank=True, default=list, size=None
            ),
        ),
        migrations.AddField(
            model_name="movietag",
            name="aliases",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255), blank=True, default=list, size=None
            ),
        ),
        migrations.AddField(
            model_name="showtag",
            name="aliases",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255), blank=True, default=list, size=None
            ),
        ),
    ]
