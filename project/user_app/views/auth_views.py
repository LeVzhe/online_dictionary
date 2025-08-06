from rest_framework import (
    decorators,
    response,
    status,
    viewsets,
)
from rest_framework.permissions import AllowAny

from user_app import models as user_app_models
from user_app import serializers as user_app_serializers


class AuthViewset(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ["register_user"]:
            return user_app_serializers.RegistrationSerializer
        return super().get_serializer_class()

    @decorators.action(
        detail=False,
        methods=["POST"],
    )
    def register_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user = user_app_models.User.objects.create_user(
            username=validated_data["login"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        user.save()

        return response.Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
