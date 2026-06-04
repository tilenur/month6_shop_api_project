from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import ConfirmationCode, CustomUser


class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):

    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email

        raise ValidationError("User already exists!")


class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.IntegerField(
        min_value=100000,
        max_value=999999
    )

    def validate(self, attrs):
        user_id = attrs.get("user_id")
        code = attrs.get("code")

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError(
                "User does not exist!"
            )

        try:
            confirmation_code = ConfirmationCode.objects.get(
                user=user
            )
        except ConfirmationCode.DoesNotExist:
            raise ValidationError(
                "Confirmation code not found!"
            )

        if confirmation_code.code != code:
            raise ValidationError(
                "Invalid confirmation code!"
            )

        return attrs