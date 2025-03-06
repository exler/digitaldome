from django.contrib import admin

from tracking.models import TrackingObject


@admin.register(TrackingObject)
class TrackingObjectAdmin(admin.ModelAdmin):
    list_select_related = ("user",)
    list_display = ("content_object", "user", "status", "rating", "created_at")
