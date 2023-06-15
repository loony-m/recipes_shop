from django.contrib import admin
from .models import Tags


@admin.register(Tags)
class AdminTags(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color'
    )
