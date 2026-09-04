import secrets
from django.conf import settings
from django.core.mail import send_mail


def generate_otp():
    """
    Generate a secure 6-digit OTP.
    """
    return f"{secrets.randbelow(1_000_000):06d}"


def send_verification_email(email, otp):
    """
    Send the email verification OTP to the user.
    """

    send_mail(
        subject="Verify Your Email Address",
        message=(
            "Hello,\n\n"
            "Thank you for signing up!\n\n"
            "To verify your email address, please use the following "
            f"one-time password (OTP):\n\n"
            f"Your OTP: {otp}\n\n"
            "This OTP is valid for 10 minutes. For your security, "
            "please do not share this OTP with anyone.\n\n"
            "If you did not request this verification, you can safely "
            "ignore this email.\n\n"
            "Thank you,\n"
            "The Support Team"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


def send_password_reset_otp_email(email, otp):
    subject = "Password Reset OTP"

    message = f"""
Hello,

We received a request to reset the password for your account.

Your password reset OTP is:

{otp}

This OTP is valid for 10 minutes. For your security, please do not share this OTP with anyone.

If you did not request a password reset, you can safely ignore this email.

Regards,
Your Support Team
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
