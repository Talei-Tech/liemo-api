from django.contrib import admin
from .models import Store, StoreLink


class StoreLinkInline(admin.TabularInline):
    model = StoreLink
    extra = 1


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'admin', 'status', 'is_live', 'is_verified', 'avg_rating']
    list_filter = ['status', 'is_live', 'is_verified']
    search_fields = ['name', 'admin__email']
    inlines = [StoreLinkInline]
