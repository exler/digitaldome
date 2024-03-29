# Generated by Django 4.2.6 on 2023-10-19 14:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tracking", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="userstats",
            name="user",
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="trackingobject",
            name="content_type",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="contenttypes.contenttype"),
        ),
        migrations.AddField(
            model_name="trackingobject",
            name="user",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name="trackingobject",
            index=models.Index(fields=["object_id", "content_type"], name="tracking_tr_object__10fa5f_idx"),
        ),
        migrations.AddIndex(
            model_name="trackingobject",
            index=models.Index(fields=["user", "status"], name="tracking_tr_user_id_f4aaa7_idx"),
        ),
        migrations.AddConstraint(
            model_name="trackingobject",
            constraint=models.UniqueConstraint(
                fields=("object_id", "content_type", "user"), name="unique_tracking_object"
            ),
        ),
    ]
