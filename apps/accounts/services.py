# business logic layer

from .exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)
from .repositories import create_user, get_user_by_email


def signup_user(validated_data):
    full_name = validated_data["full_name"]
    email = validated_data["email"]
    password = validated_data["password"]

    # Check whether the email is already registered
    existing_user = get_user_by_email(email)

    if existing_user:
        raise EmailAlreadyExistsException()

    # Create the user
    user = create_user(
        full_name=full_name,
        email=email,
        password=password,
    )

    return {
        "message": "Account created successfully.",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        },
    }


def login_user(validated_data):
    email = validated_data["email"]
    password = validated_data["password"]

    # Find user by email
    user = get_user_by_email(email)

    # Check credentials
    if not user or not user.check_password(password):
        raise InvalidCredentialsException()

    return {
        "message": "Login successful.",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        },
    }