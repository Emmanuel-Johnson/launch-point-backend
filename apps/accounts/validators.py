import re
from rest_framework import serializers


def validate_full_name(value):
    value = value.strip()

    if len(value) < 2:
        raise serializers.ValidationError(
            "Full name must be at least 2 characters."
        )

    if len(value) > 50:
        raise serializers.ValidationError("Full name is too long.")

    if not re.fullmatch(
        r"[^\W\d_]+(?:[ '-][^\W\d_]+)*",
        value,
        re.UNICODE,
    ):
        raise serializers.ValidationError("Please enter a valid full name.")

    return value


def validate_password(value):
    if len(value) < 8:
        raise serializers.ValidationError(
            "Password must be at least 8 characters."
        )

    if len(value) > 128:
        raise serializers.ValidationError("Password is too long.")

    if value != value.strip():
        raise serializers.ValidationError(
            "Password cannot start or end with spaces."
        )

    if not re.search(r"[A-Z]", value):
        raise serializers.ValidationError(
            "Must contain at least one uppercase letter."
        )

    if not re.search(r"[a-z]", value):
        raise serializers.ValidationError(
            "Must contain at least one lowercase letter."
        )

    if not re.search(r"[0-9]", value):
        raise serializers.ValidationError(
            "Must contain at least one number."
        )

    if not re.search(r"[^A-Za-z0-9]", value):
        raise serializers.ValidationError(
            "Must contain at least one special character."
        )

    return value