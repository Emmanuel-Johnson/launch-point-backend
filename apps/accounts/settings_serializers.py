from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )
    new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )
    confirm_new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate_current_password(self, value):
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("Your current password is incorrect.")

        return value

    def validate(self, attrs):
        user = self.context["request"].user
        new_password = attrs["new_password"]
        confirm_new_password = attrs["confirm_new_password"]

        if new_password != confirm_new_password:
            raise serializers.ValidationError(
                {
                    "confirm_new_password": (
                        "New password and confirm password do not match."
                    )
                }
            )

        if attrs["current_password"] == new_password:
            raise serializers.ValidationError(
                {
                    "new_password": (
                        "New password must be different from your current password."
                    )
                }
            )

        try:
            validate_password(new_password, user=user)
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                {"new_password": error.messages}
            ) from error

        return attrs
