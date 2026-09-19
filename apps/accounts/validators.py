import re

from rest_framework import serializers


def validate_full_name(value):
    """
    Validate and normalize a full name.

    Trims surrounding whitespace and requires a length of 2-50 characters
    consisting of letters (any script), with single spaces, apostrophes, or
    hyphens allowed between name parts.

    Returns:
        str: The trimmed full name.

    Raises:
        ValidationError: If the name is too short, too long, or contains
            disallowed characters.
    """
    value = value.strip()

    if len(value) < 2:
        raise serializers.ValidationError("Full name must be at least 2 characters.")

    if len(value) > 50:
        raise serializers.ValidationError("Full name is too long.")

    # Accept letters of any script, joined only by single spaces, apostrophes,
    # or hyphens between name parts (e.g. "Anne-Marie", "O'Brien"). [^\W\d_]
    # matches a Unicode letter while excluding digits and underscores.
    if not re.fullmatch(
        r"[^\W\d_]+(?:[ '-][^\W\d_]+)*",
        value,
        re.UNICODE,
    ):
        raise serializers.ValidationError("Please enter a valid full name.")

    return value


def validate_password(value):
    """
    Validate a password against the application's complexity requirements.

    Enforces a length of 8-128 characters, no leading or trailing whitespace,
    and at least one uppercase letter, one lowercase letter, one digit, and one
    special (non-alphanumeric) character.

    Returns:
        str: The validated password, unchanged.

    Raises:
        ValidationError: If any requirement is not met.
    """
    if len(value) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters.")

    if len(value) > 128:
        raise serializers.ValidationError("Password is too long.")

    if value != value.strip():
        raise serializers.ValidationError("Password cannot start or end with spaces.")

    if not re.search(r"[A-Z]", value):
        raise serializers.ValidationError("Must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", value):
        raise serializers.ValidationError("Must contain at least one lowercase letter.")

    if not re.search(r"[0-9]", value):
        raise serializers.ValidationError("Must contain at least one number.")

    if not re.search(r"[^A-Za-z0-9]", value):
        raise serializers.ValidationError(
            "Must contain at least one special character."
        )

    return value
