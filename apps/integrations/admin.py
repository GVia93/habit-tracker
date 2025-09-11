from django.contrib import admin

from .models import TelegramProfile


@admin.register(TelegramProfile)
class TelegramProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "telegram_id", "username", "is_active", "linked_at")
    search_fields = ("user__email", "telegram_id", "username")
    list_filter = ("is_active", "linked_at")
