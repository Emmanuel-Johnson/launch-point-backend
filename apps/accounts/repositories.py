import logging

from django.db import DatabaseError
from django.utils import timezone

from .models import EmailVerificationOTP, PasswordResetOTP, PasswordResetToken, User

logger = logging.getLogger(__name__)


def create_user(**validated_data):
    """
    Create and persist a new user.

    Delegates to the user manager's create_user, which hashes the supplied
    password before saving.
    """

    try:
        return User.objects.create_user(**validated_data)
    except DatabaseError:
        logger.exception("Database error while creating user")
        raise


def get_user_by_email(email):
    """
    Retrieve a user by their email address.

    Returns:
        User | None: The matching user, or None if no user exists.
    """

    return User.objects.filter(email=email).first()


def get_verified_user_by_email(email):
    """
    Retrieve a user by email, restricted to accounts whose email is verified.

    Returns:
        User | None: The matching verified user, or None if none exists.
    """
    return User.objects.filter(
        email=email,
        email_verified=True,
    ).first()


def create_email_verification_otp(user, otp_hash, expires_at):

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
    Return the most recently created email verification OTP for the user.

    Returns:
        EmailVerificationOTP | None: The latest OTP, or None if the user has none.
    """

    return (
        EmailVerificationOTP.objects.filter(user=user).order_by("-created_at").first()
    )


def delete_email_verification_otps(user):

    try:
        EmailVerificationOTP.objects.filter(user=user).delete()
    except DatabaseError:
        logger.exception(
            "Database error while deleting email verification OTPs user_id=%s",
            user.id,
        )
        raise


def verify_user_email(user):
    """
    Persist the user's verified-email flag.

    Writes only the email_verified and updated_at columns via update_fields.
    """
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
    """
    Return the most recently created password reset OTP for the user.

    Returns:
        PasswordResetOTP | None: The latest OTP, or None if the user has none.
    """
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
    """
    Look up an unused password reset token by its hash.

    Only tokens that have not been marked used (used_at is null) are returned.

    Returns:
        PasswordResetToken | None: The matching active token, or None.
    """
    return (
        PasswordResetToken.objects.filter(
            token_hash=token_hash,
            used_at__isnull=True,
        )
        # Eager-load the user to avoid a second query when the caller reads token.user.
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
    """
    Stamp a password reset token as used by recording the current time in used_at.
    """
    # Setting used_at is what excludes the token from future
    # get_password_reset_token lookups (which filter used_at__isnull=True).
    token.used_at = timezone.now()
    token.save(update_fields=["used_at"])


def update_user_password(user, new_password):
    """
    Hash and persist a new password for the user.

    set_password stores a hashed value; only the password column is written.
    """
    user.set_password(new_password)
    user.save(update_fields=["password"])


def get_user_by_google_id(google_id):
    """
    Retrieve a user by their linked Google account id.

    Returns:
        User | None: The matching user, or None if no user is linked to the id.
    """
    return User.objects.filter(google_id=google_id).first()


def create_google_user(
    *,
    full_name,
    email,
    google_id,
):
    """
    Create and persist a user backed by a Google account.

    The record is stored as email-verified and active with an unusable
    password (set_unusable_password), so no usable password hash is saved.
    """
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
