import hashlib
import logging
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import (
    check_password,
    make_password,
)
from django.utils import timezone
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework_simplejwt.tokens import RefreshToken

from .exceptions import (
    EmailAlreadyExistsException,
    EmailAlreadyVerifiedException,
    EmailVerificationOTPExpiredException,
    InvalidCredentialsException,
    InvalidEmailVerificationOTPException,
    InvalidGoogleTokenException,
    InvalidPasswordResetOTPException,
    InvalidPasswordResetTokenException,
    OTPResendTooSoonException,
    PasswordResetOTPExpiredException,
    PasswordResetTokenExpiredException,
    SamePasswordException,
)
from .repositories import (
    create_email_verification_otp,
    create_google_user,
    create_password_reset_otp,
    create_password_reset_token,
    create_user,
    delete_email_verification_otps,
    delete_password_reset_otps,
    delete_password_reset_tokens,
    get_latest_email_verification_otp,
    get_latest_password_reset_otp,
    get_password_reset_token,
    get_user_by_email,
    get_user_by_google_id,
    get_verified_user_by_email,
    link_google_account,
    mark_password_reset_token_used,
    update_user_password,
    verify_user_email,
)
from .utils import (
    generate_otp,
    send_password_reset_otp_email,
    send_verification_email,
)

logger = logging.getLogger(__name__)


def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def signup_user(validated_data):
    full_name = validated_data["full_name"]
    email = validated_data["email"]
    password = validated_data["password"]

    logger.info("Signup attempt")

    existing_user = get_user_by_email(email)

    if existing_user and existing_user.email_verified:
        logger.warning("Signup rejected: email already exists")
        raise EmailAlreadyExistsException()

    if existing_user:
        user = existing_user
        logger.info("Resuming signup for unverified user")
    else:
        user = create_user(
            full_name=full_name,
            email=email,
            password=password,
        )
        logger.info("User created successfully user_id=%s", user.id)

    delete_email_verification_otps(user)

    otp = generate_otp()

    otp_hash = make_password(otp)

    expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

    create_email_verification_otp(
        user=user,
        otp_hash=otp_hash,
        expires_at=expires_at,
    )

    send_verification_email(
        user.email,
        otp,
    )

    return {
        "message": ("Account created successfully. Please verify your email."),
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        },
    }


def verify_email_otp(email, otp):
    logger.info("Email verification attempt")
    user = get_user_by_email(email)

    if not user:
        logger.warning("Email verification failed: user not found")
        raise InvalidEmailVerificationOTPException()

    if user.email_verified:
        logger.warning(
            "Email verification rejected: already verified user_id=%s",
            user.id,
        )
        raise EmailAlreadyVerifiedException()

    verification_otp = get_latest_email_verification_otp(user)

    if not verification_otp:
        logger.warning(
            "Email verification failed: no OTP found user_id=%s",
            user.id,
        )
        raise InvalidEmailVerificationOTPException()

    if not check_password(
        otp,
        verification_otp.otp_hash,
    ):
        logger.warning(
            "Email verification failed: invalid OTP user_id=%s",
            user.id,
        )
        raise InvalidEmailVerificationOTPException()

    if timezone.now() >= verification_otp.expires_at:
        logger.warning(
            "Email verification failed: expired OTP user_id=%s",
            user.id,
        )
        raise EmailVerificationOTPExpiredException()

    verify_user_email(user)

    logger.info(
        "Email verified successfully user_id=%s",
        user.id,
    )

    delete_email_verification_otps(user)

    tokens = generate_tokens_for_user(user)

    return {
        "message": "Email verified successfully.",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        },
        "tokens": tokens,
    }


def resend_verification_otp(email):
    logger.info("Verification OTP resend requested")

    user = get_user_by_email(email)

    if not user:
        logger.warning("Verification OTP resend failed: user not found")
        raise InvalidEmailVerificationOTPException()

    if user.email_verified:
        logger.warning(
            "Verification OTP resend rejected: already verified user_id=%s",
            user.id,
        )
        raise EmailAlreadyVerifiedException()

    latest_otp = get_latest_email_verification_otp(user)

    if latest_otp:
        cooldown_end = latest_otp.created_at + timedelta(
            seconds=settings.OTP_RESEND_COOLDOWN_SECONDS
        )

        if timezone.now() < cooldown_end:
            logger.warning(
                "Verification OTP resend rejected: cooldown active user_id=%s",
                user.id,
            )
            raise OTPResendTooSoonException()

    delete_email_verification_otps(user)

    otp = generate_otp()

    otp_hash = make_password(otp)

    expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

    create_email_verification_otp(
        user=user,
        otp_hash=otp_hash,
        expires_at=expires_at,
    )

    send_verification_email(
        email=user.email,
        otp=otp,
    )

    logger.info(
        "Verification OTP resent successfully user_id=%s",
        user.id,
    )

    return {"message": "A new verification OTP has been sent."}


def login_user(validated_data):
    email = validated_data["email"]
    password = validated_data["password"]

    logger.info("Login attempt")

    user = get_user_by_email(email)

    if (
        not user
        or not user.check_password(password)
        or not user.email_verified
        or not user.is_active
        or user.is_superuser
    ):
        logger.warning("Login failed")
        raise InvalidCredentialsException()

    tokens = generate_tokens_for_user(user)

    logger.info("Login successful user_id=%s", user.id)

    return {
        "message": "Login successful.",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        },
        "tokens": tokens,
    }


def forgot_password(email):
    logger.info("Password reset requested")

    user = get_verified_user_by_email(email)

    if not user:
        logger.info("Password reset requested for non-existing email")
        return {
            "message": (
                "If an account exists for this email, "
                "a password reset OTP has been sent."
            )
        }

    delete_password_reset_otps(user)

    otp = generate_otp()

    logger.info(
        "Password reset OTP generated user_id=%s",
        user.id,
    )

    otp_hash = make_password(otp)

    expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

    create_password_reset_otp(
        user=user,
        otp_hash=otp_hash,
        expires_at=expires_at,
    )

    send_password_reset_otp_email(
        email=user.email,
        otp=otp,
    )

    return {
        "message": (
            "If an account exists for this email, a password reset OTP has been sent."
        )
    }


def verify_password_reset_otp(email, otp):
    logger.info("Password reset OTP verification attempt")

    user = get_verified_user_by_email(email)

    if not user:
        logger.warning("Password reset OTP verification failed: user not found")
        raise InvalidPasswordResetOTPException()

    password_reset_otp = get_latest_password_reset_otp(user)

    if not password_reset_otp:
        logger.warning(
            "Password reset OTP verification failed: no OTP found user_id=%s",
            user.id,
        )
        raise InvalidPasswordResetOTPException()

    if not check_password(
        otp,
        password_reset_otp.otp_hash,
    ):
        logger.warning(
            "Password reset OTP verification failed: invalid OTP user_id=%s",
            user.id,
        )
        raise InvalidPasswordResetOTPException()

    if timezone.now() >= password_reset_otp.expires_at:
        logger.warning(
            "Password reset OTP verification failed: expired OTP user_id=%s",
            user.id,
        )
        raise PasswordResetOTPExpiredException()

    delete_password_reset_otps(user)

    delete_password_reset_tokens(user)

    raw_token, token_hash = generate_password_reset_token()

    expires_at = timezone.now() + timedelta(
        minutes=settings.PASSWORD_RESET_TOKEN_EXPIRY_MINUTES
    )

    create_password_reset_token(
        user=user,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    logger.info(
        "Password reset OTP verified successfully user_id=%s",
        user.id,
    )

    return {
        "message": "OTP verified successfully.",
        "reset_token": raw_token,
    }


def resend_password_reset_otp(email):
    logger.info("Password reset OTP resend requested")

    user = get_verified_user_by_email(email)

    if not user:
        logger.warning("Password reset OTP resend failed: user not found")
        raise InvalidCredentialsException()

    latest_otp = get_latest_password_reset_otp(user)

    if latest_otp:
        cooldown_end = latest_otp.created_at + timedelta(
            seconds=settings.OTP_RESEND_COOLDOWN_SECONDS
        )

        if timezone.now() < cooldown_end:
            logger.warning(
                "Password reset OTP resend rejected: cooldown active user_id=%s",
                user.id,
            )
            raise OTPResendTooSoonException()
    delete_password_reset_otps(user)

    otp = generate_otp()

    otp_hash = make_password(otp)

    expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

    create_password_reset_otp(
        user=user,
        otp_hash=otp_hash,
        expires_at=expires_at,
    )

    send_password_reset_otp_email(
        email=user.email,
        otp=otp,
    )

    logger.info(
        "Password reset OTP resent successfully user_id=%s",
        user.id,
    )

    return {"message": "A new password reset OTP has been sent."}


def generate_password_reset_token():
    raw_token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    return raw_token, token_hash


def reset_password(reset_token, new_password):

    logger.info("Password reset attempt")

    token_hash = hashlib.sha256(reset_token.encode()).hexdigest()

    token = get_password_reset_token(token_hash)

    if not token:
        logger.warning("Password reset failed: invalid token")
        raise InvalidPasswordResetTokenException()

    if token.expires_at <= timezone.now():
        logger.warning("Password reset failed: expired token")
        raise PasswordResetTokenExpiredException()

    user = token.user

    if user.check_password(new_password):
        logger.warning(
            "Password reset failed: same password user_id=%s",
            user.id,
        )
        raise SamePasswordException()

    update_user_password(user, new_password)

    mark_password_reset_token_used(token)

    delete_password_reset_tokens(user)

    logger.info(
        "Password reset successful user_id=%s",
        user.id,
    )

    return {"message": "Password reset successfully."}


def google_authenticate(id_token_string):

    logger.info("Google authentication attempt")

    try:
        idinfo = id_token.verify_oauth2_token(
            id_token_string,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )

    except ValueError:
        logger.warning("Google authentication failed: invalid token")
        raise InvalidGoogleTokenException()

    google_id = idinfo.get("sub")
    email = idinfo.get("email")
    email_verified = idinfo.get("email_verified")
    full_name = idinfo.get("name")

    if not google_id or not email:
        logger.warning(
            "Google authentication failed: missing google_id or email in token"
        )
        raise InvalidGoogleTokenException()

    if not email_verified:
        logger.warning("Google authentication failed: email not verified by Google")
        raise InvalidGoogleTokenException()

    email = email.lower()

    user = get_user_by_google_id(google_id)

    if user:
        if not user.is_active:
            logger.warning(
                "Google authentication failed: inactive user user_id=%s",
                user.id,
            )
            raise InvalidGoogleTokenException()

    else:
        user = get_verified_user_by_email(email)

        if user:
            if user.google_id and user.google_id != google_id:
                logger.warning(
                    "Google authentication failed: email linked to a "
                    "different Google account user_id=%s",
                    user.id,
                )
                raise InvalidGoogleTokenException()

            link_google_account(user, google_id)

            logger.info(
                "Google account linked to existing user user_id=%s",
                user.id,
            )

        else:
            user = create_google_user(
                full_name=full_name or email.split("@")[0],
                email=email,
                google_id=google_id,
            )

            logger.info(
                "Google user created successfully user_id=%s",
                user.id,
            )

    if not user.is_active:
        logger.warning(
            "Google authentication failed: inactive account user_id=%s",
            user.id,
        )
        raise InvalidGoogleTokenException()

    tokens = generate_tokens_for_user(user)

    logger.info(
        "Google authentication successful user_id=%s",
        user.id,
    )

    return {
        "message": "Google authentication successful.",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        },
        "tokens": tokens,
    }


def admin_login_user(validated_data):
    email = validated_data["email"]
    password = validated_data["password"]

    logger.info("Admin login attempt")

    user = get_user_by_email(email)

    if (
        not user
        or not user.check_password(password)
        or not user.is_active
        or not user.is_staff
        or not user.is_superuser
    ):
        logger.warning("Admin login failed")
        raise InvalidCredentialsException()

    tokens = generate_tokens_for_user(user)

    logger.info("Admin login successful user_id=%s", user.id)

    return {
        "message": "Admin login successful.",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        },
        "tokens": tokens,
    }
