from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TelegramProfileViewSet

app_name = "integrations"

router = DefaultRouter()
router.register(r"telegram-profiles", TelegramProfileViewSet, basename="telegram-profile")

urlpatterns = [
    path("", include(router.urls)),
]
