import random
from datetime import timedelta

from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers

from .models import User


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = ["full_name", "email", "password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )

        return value

    def create(self, validated_data):
        # Create the user
        user = User.objects.create_user(
            **validated_data
        )

        # Generate a 6-digit verification code
        code = str(random.randint(100000, 999999))

        # Save OTP and expiration time
        user.email_verification_code = code
        user.email_verification_code_expires_at = (
            timezone.now() + timedelta(minutes=10)
        )

        user.save(
            update_fields=[
                "email_verification_code",
                "email_verification_code_expires_at",
            ]
        )

        # Send verification email
        send_mail(
            subject="Verify your Launch Point account",
            message=(
                f"Your verification code is: {code}\n\n"
                "This code will expire in 10 minutes."
            ),
            from_email=None,
            recipient_list=[user.email],
        )

        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    code = serializers.CharField(
        min_length=6,
        max_length=6
    )

    def validate(self, attrs):
        email = attrs["email"]
        code = attrs["code"]

        # Find user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "User not found."}
            )

        # Check if already verified
        if user.email_verified:
            raise serializers.ValidationError(
                {"email": "Email is already verified."}
            )

        # Check OTP
        if user.email_verification_code != code:
            raise serializers.ValidationError(
                {"code": "Invalid verification code."}
            )

        # Check OTP expiration
        if (
            not user.email_verification_code_expires_at
            or user.email_verification_code_expires_at < timezone.now()
        ):
            raise serializers.ValidationError(
                {"code": "Verification code has expired."}
            )

        # Pass user to save()
        attrs["user"] = user

        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]

        user.email_verified = True
        user.email_verification_code = None
        user.email_verification_code_expires_at = None

        user.save(
            update_fields=[
                "email_verified",
                "email_verification_code",
                "email_verification_code_expires_at",
            ]
        )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        # Authenticate user
        user = authenticate(
            email=email,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        # Require email verification
        if not user.email_verified:
            raise serializers.ValidationError(
                "Please verify your email before logging in."
            )

        # Pass user to the view
        attrs["user"] = user

        return attrs