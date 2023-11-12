from django.contrib import admin

from tracking.models import TrackingObject


@admin.register(TrackingObject)
class TrackingObjectAdmin(admin.ModelAdmin):
    pass
