from django.contrib import admin
from .models import Polygon


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at'
    )
