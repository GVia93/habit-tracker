from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Админка для модели Habit:
    - list_display: основные поля для списка
    - search_fields: поиск по действию и месту
    - list_filter: фильтры по пользователю, публичности и приятности
    """

    list_display = ("id", "user", "action", "place", "time", "is_pleasant", "is_public", "created_at")
    search_fields = ("action", "place", "user__email")
    list_filter = ("is_pleasant", "is_public", "time", "user")
    ordering = ("-created_at",)
