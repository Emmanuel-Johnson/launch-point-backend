from .models import User, EmailVerificationOTP, PasswordResetOTP


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
    return EmailVerificationOTP.objects.filter(
        user=user
    ).order_by("-created_at").first()


def delete_email_verification_otps(user):
    """
    Delete all existing OTPs for the given user.
    """
    EmailVerificationOTP.objects.filter(
        user=user
    ).delete()


def create_password_reset_otp(user, otp_hash, expires_at):
    return PasswordResetOTP.objects.create(
        user=user,
        otp_hash=otp_hash,
        expires_at=expires_at,
    )


def get_latest_password_reset_otp(user):
    return (
        PasswordResetOTP.objects
        .filter(user=user)
        .order_by("-created_at")
        .first()
    )


def delete_password_reset_otps(user):
    PasswordResetOTP.objects.filter(user=user).delete()
