from django.contrib import admin
from .models import SoftDeleteModel
from django.utils.html import format_html


class SoftDeleteAdmin(admin.ModelAdmin):
    list_filter = ['is_deleted']
    actions = ['soft_delete_selected', 'restore_selected']

    def get_queryset(self, request):
        # Show all, including soft-deleted
        return self.model.all_objects.all()

    def soft_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
        self.message_user(request, f"{queryset.count()} item(s) soft-deleted.")

    soft_delete_selected.short_description = "Soft delete selected records"

    def restore_selected(self, request, queryset):
        for obj in queryset:
            obj.restore()
        self.message_user(request, f"{queryset.count()} item(s) restored.")

    restore_selected.short_description = "Restore selected records"


