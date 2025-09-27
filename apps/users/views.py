from rest_framework import generics, permissions

from .serializers import RegisterSerializer


class RegisterAPIView(generics.CreateAPIView):
    """POST /auth/register — регистрация по email+password."""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
