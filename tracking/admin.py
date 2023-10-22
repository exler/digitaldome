from django.contrib import admin

from tracking.models import TrackingObject, UserStats


@admin.register(TrackingObject)
class TrackingObjectAdmin(admin.ModelAdmin):
    pass


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    pass
