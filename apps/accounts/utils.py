import logging
import secrets

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def generate_otp():

    return f"{secrets.randbelow(1_000_000):06d}"


def send_verification_email(email, otp):
    subject = "Verify Your Email Address"

    message = (
        "Hello,\n\n"
        "Thank you for signing up!\n\n"
        "To verify your email address, please use the following "
        f"one-time password (OTP):\n\n"
        f"Your OTP: {otp}\n\n"
        f"This OTP is valid for {settings.OTP_EXPIRY_MINUTES} minutes. "
        "For your security, please do not share this OTP with anyone.\n\n"
        "If you did not request this verification, you can safely "
        "ignore this email.\n\n"
        "Thank you,\n"
        "The Support Team"
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Failed to send verification email")
        raise


def send_password_reset_otp_email(email, otp):
    subject = "Password Reset OTP"

    message = (
        "Hello,\n\n"
        "We received a request to reset the password for your account.\n\n"
        "Your password reset OTP is:\n\n"
        f"{otp}\n\n"
        f"This OTP is valid for {settings.OTP_EXPIRY_MINUTES} minutes.\n\n"
        "For your security, please do not share this OTP with anyone.\n\n"
        "If you did not request a password reset, you can safely "
        "ignore this email.\n\n"
        "Regards,\n"
        "The Support Team"
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
    except Exception:
        logger.exception("Failed to send password reset email")
        raise
