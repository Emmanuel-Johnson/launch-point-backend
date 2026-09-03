from rest_framework import serializers
from .validators import validate_full_name, validate_password


class SignupSerializer(serializers.Serializer):
    full_name = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=50,
        validators=[validate_full_name],
    )

    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        max_length=254,
    )

    password = serializers.CharField(
        required=True,
        allow_blank=False,
        write_only=True,
        max_length=128,
        validators=[validate_password],
    )

    def validate_email(self, value):
        return value.strip().lower()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        max_length=254,
    )

    password = serializers.CharField(
        required=True,
        allow_blank=False,
        write_only=True,
        max_length=128,
    )

    def validate_email(self, value):
        return value.strip().lower()


class VerifyEmailOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(
        required=True,
        allow_blank=False,
        min_length=6,
        max_length=6,
    )

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "OTP must contain only numbers."
            )

        return value
