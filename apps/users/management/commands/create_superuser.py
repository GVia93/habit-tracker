from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создаёт суперпользователя с предопределёнными данными"

    def handle(self, *args, **options):
        User = get_user_model()

        if not User.objects.filter(email="admin@admin.com").exists():
            User.objects.create_superuser(
                email="admin@admin.com",
                password="admin",
            )
            self.stdout.write(self.style.SUCCESS("Суперпользователь admin@admin.com успешно создан"))
        else:
            self.stdout.write(self.style.WARNING("Суперпользователь admin@admin.com уже существует"))
