from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated


from . import serializers

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    serializer_class = serializers.UserCreateSerializer
    permission_classes = [AllowAny]
