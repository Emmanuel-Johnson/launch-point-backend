# database access layer.

from .models import User


def create_user(**validated_data):
    """
    Create and return a new user.
    """
    return User.objects.create_user(**validated_data)


def get_user_by_email(email):
    """
    Return the user with the given email, or None if not found.
    """
    return User.objects.filter(email=email).first()