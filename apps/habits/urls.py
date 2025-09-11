from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HabitViewSet, PublicHabitList

app_name = "habits"

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")

urlpatterns = [
    path("habits/public/", PublicHabitList.as_view(), name="habits-public"),
    path("", include(router.urls)),
]
