from __future__ import annotations

from rest_framework import generics, permissions, viewsets

from utils.permissions import IsOwnerOrReadOnly

from .models import Habit
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD по своим привычкам. Чужие недоступны в queryset/объектных правах."""

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Habit.objects.none()
        return Habit.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer: HabitSerializer) -> None:
        serializer.save(user=self.request.user)


class PublicHabitList(generics.ListAPIView):
    """GET /habits/public/ — публичные привычки доступны без авторизации."""

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
