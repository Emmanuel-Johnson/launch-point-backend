from .models import EmailVerificationOTP, PasswordResetOTP, PasswordResetToken, User


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


def get_verified_user_by_email(email):
    return User.objects.filter(
        email=email,
        email_verified=True,
    ).first()


def create_email_verification_otp(user, otp_hash, expires_at):
    """
    Create and return a new email verification OTP.
    """
    return EmailVerificationOTP.objects.create(
        user=user,
        otp_hash=otp_hash,
        expires_at=expires_at,
    )


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
    EmailVerificationOTP.objects.filter(user=user).delete()


def create_password_reset_otp(user, otp_hash, expires_at):
    return PasswordResetOTP.objects.create(
        user=user,
        otp_hash=otp_hash,
        expires_at=expires_at,
    )


def get_latest_password_reset_otp(user):
    return PasswordResetOTP.objects.filter(user=user).order_by("-created_at").first()


def delete_password_reset_otps(user):
    PasswordResetOTP.objects.filter(user=user).delete()


def create_password_reset_token(
    user,
    token_hash,
    expires_at,
):
    return PasswordResetToken.objects.create(
        user=user,
        token_hash=token_hash,
        expires_at=expires_at,
    )


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
    PasswordResetToken.objects.filter(user=user).delete()


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
    user.save()

    return user
