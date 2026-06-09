from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .serializers import (
    RegisterValidateSerializer,
    AuthValidateSerializer,
    ConfirmationSerializer,
)

from .models import ConfirmationCode
from users.models import CustomUser

import random


class AuthorizationAPIView(CreateAPIView):
    serializer_class = AuthValidateSerializer

    def post(self, request):

        serializer = AuthValidateSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"]
        )

        if user:

            if not user.is_active:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={
                        "error":
                        "User account is not activated yet!"
                    }
                )

            token, _ = Token.objects.get_or_create(
                user=user
            )

            return Response(
                data={"key": token.key}
            )

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={
                "error":
                "User credentials are wrong!"
            }
        )


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            is_active=False
        )

        code = random.randint(
            100000,
            999999
        )

        ConfirmationCode.objects.create(
            user=user,
            code=code
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "user_id": user.id,
                "confirmation_code": code
            }
        )


class ConfirmAPIView(CreateAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request):

        serializer = ConfirmationSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]

        user = CustomUser.objects.get(
            email=email
        )

        user.is_active = True
        user.save()

        token, _ = Token.objects.get_or_create(
            user=user
        )

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message":
                "User successfully activated",
                "key": token.key
            }
        )