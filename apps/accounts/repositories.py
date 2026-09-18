import logging

from django.db import DatabaseError
from django.utils import timezone

from .models import EmailVerificationOTP, PasswordResetOTP, PasswordResetToken, User

logger = logging.getLogger(__name__)


def create_user(**validated_data):
    """
    Create and return a new user.
    """
    try:
        return User.objects.create_user(**validated_data)
    except DatabaseError:
        logger.exception("Database error while creating user")
        raise


def get_user_by_email(email):
    """
    Return the user with the given email, or None if not found.
    """
    return User.objects.filter(email=email).first()


def get_verified_user_by_email(email):
    return User.objects.filter(
        email=email,
        email_verified=True,
    ).first()


def create_email_verification_otp(user, otp_hash, expires_at):
    """
    Create and return a new email verification OTP.
    """
    try:
        return EmailVerificationOTP.objects.create(
            user=user,
            otp_hash=otp_hash,
            expires_at=expires_at,
        )
    except DatabaseError:
        logger.exception(
            "Database error while creating email verification OTP user_id=%s",
            user.id,
        )
        raise


def get_latest_email_verification_otp(user):
    """
    Return the latest OTP for the given user, or None if not found.
    """
    return (
        EmailVerificationOTP.objects.filter(user=user).order_by("-created_at").first()
    )


def delete_email_verification_otps(user):
    """
    Delete all existing OTPs for the given user.
    """
    try:
        EmailVerificationOTP.objects.filter(user=user).delete()
    except DatabaseError:
        logger.exception(
            "Database error while deleting email verification OTPs user_id=%s",
            user.id,
        )
        raise


def verify_user_email(user):
    user.email_verified = True
    user.save(
        update_fields=[
            "email_verified",
            "updated_at",
        ]
    )


def create_password_reset_otp(user, otp_hash, expires_at):
    try:
        return PasswordResetOTP.objects.create(
            user=user,
            otp_hash=otp_hash,
            expires_at=expires_at,
        )
    except DatabaseError:
        logger.exception(
            "Database error while creating password reset OTP user_id=%s",
            user.id,
        )
        raise


def get_latest_password_reset_otp(user):
    return PasswordResetOTP.objects.filter(user=user).order_by("-created_at").first()


def delete_password_reset_otps(user):
    try:
        PasswordResetOTP.objects.filter(user=user).delete()
    except DatabaseError:
        logger.exception(
            "Database error while deleting password reset OTPs user_id=%s",
            user.id,
        )
        raise


def create_password_reset_token(
    user,
    token_hash,
    expires_at,
):
    try:
        return PasswordResetToken.objects.create(
            user=user,
            token_hash=token_hash,
            expires_at=expires_at,
        )
    except DatabaseError:
        logger.exception(
            "Database error while creating password reset token user_id=%s",
            user.id,
        )
        raise


def get_password_reset_token(token_hash):
    return (
        PasswordResetToken.objects.filter(
            token_hash=token_hash,
            used_at__isnull=True,
        )
        .select_related("user")
        .first()
    )


def delete_password_reset_tokens(user):
    try:
        PasswordResetToken.objects.filter(user=user).delete()
    except DatabaseError:
        logger.exception(
            "Database error while deleting password reset tokens user_id=%s",
            user.id,
        )
        raise


def mark_password_reset_token_used(token):
    token.used_at = timezone.now()
    token.save(update_fields=["used_at"])


def update_user_password(user, new_password):
    user.set_password(new_password)
    user.save(update_fields=["password"])


def get_user_by_google_id(google_id):
    return User.objects.filter(google_id=google_id).first()


def create_google_user(
    *,
    full_name,
    email,
    google_id,
):
    user = User(
        full_name=full_name,
        email=email,
        google_id=google_id,
        email_verified=True,
        is_active=True,
    )

    user.set_unusable_password()

    try:
        user.save()
    except DatabaseError:
        logger.exception("Database error while creating Google user")
        raise

    return user


def link_google_account(user, google_id):
    user.google_id = google_id
    user.save(update_fields=["google_id"])
