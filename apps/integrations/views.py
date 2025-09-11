from rest_framework.viewsets import ModelViewSet

from .models import TelegramProfile
from .serializers import TelegramProfileSerializer


class TelegramProfileViewSet(ModelViewSet):
    """
    ViewSet для CRUD-операций с TelegramProfile.

    Особенности:
    - queryset ограничен текущим пользователем: каждый видит только свой профиль;
    - при создании user подставляется автоматически из `request.user` в сериализаторе;
    - стандартные действия DRF:
        * list (GET /telegram-profiles/)
        * retrieve (GET /telegram-profiles/{id}/)
        * create (POST /telegram-profiles/)
        * update/partial_update (PUT/PATCH /telegram-profiles/{id}/)
        * destroy (DELETE /telegram-profiles/{id}/)
    """

    pagination_class = None
    serializer_class = TelegramProfileSerializer
    queryset = TelegramProfile.objects.all()

    def get_queryset(self):
        """Фильтруем queryset, чтобы вернуть только профиль текущего пользователя."""
        return TelegramProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создаём профиль, user автоматически берётся в serializer.create()."""
        serializer.save()
