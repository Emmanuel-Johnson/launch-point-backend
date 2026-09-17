from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import (
    check_password,
    make_password,
)
from .exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    InvalidEmailVerificationOTPException,
    EmailVerificationOTPExpiredException,
    EmailAlreadyVerifiedException,
    EmailNotVerifiedException,
    OTPResendTooSoonException,
    InvalidPasswordResetOTPException,
    PasswordResetOTPExpiredException,
    OTPVerificationAttemptsExceededException,
    PasswordResetOTPAttemptsExceededException,
    InvalidPasswordResetTokenException,
    PasswordResetTokenExpiredException,
    SamePasswordException,
)
from .repositories import (
    create_user,
    get_user_by_email,
    get_verified_user_by_email,
    create_email_verification_otp,
    get_latest_email_verification_otp,
    delete_email_verification_otps,
    create_password_reset_otp,
    delete_password_reset_otps,
    get_latest_password_reset_otp,
    create_password_reset_token,
    get_password_reset_token,
    delete_password_reset_tokens,
    get_user_by_google_id,
    create_google_user,
)
from .utils import (
    generate_otp,
    send_verification_email,
    send_password_reset_otp_email,
)
from rest_framework_simplejwt.tokens import RefreshToken
import hashlib
import secrets
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from .exceptions import InvalidGoogleTokenException


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

    # Check whether the email is already registered
    existing_user = get_user_by_email(email)

    if existing_user and existing_user.email_verified:
        raise EmailAlreadyExistsException()

    if existing_user:
        user = existing_user
    else:
        user = create_user(
            full_name=full_name,
            email=email,
            password=password,
        )

    # Delete any existing OTPs for this user
    delete_email_verification_otps(user)

    # Generate a new 6-digit OTP
    otp = generate_otp()

    # Hash the OTP before storing it
    otp_hash = make_password(otp)

    # OTP expires after 5 minutes
    expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

    # Store hashed OTP
    create_email_verification_otp(
        user=user,
        otp_hash=otp_hash,
        expires_at=expires_at,
    )

    # Send raw OTP to user's email
    send_verification_email(
        user.email,
        otp,
    )

    return {
        "message": (
            "Account created successfully. "
            "Please verify your email."
        ),
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        },
    }


def verify_email_otp(email, otp):
    # Find user by email
    user = get_user_by_email(email)

    # Do not reveal whether the email exists
    if not user:
        raise InvalidEmailVerificationOTPException()

    # Check whether email is already verified
    if user.email_verified:
        raise EmailAlreadyVerifiedException()

    # Get the latest OTP
    verification_otp = get_latest_email_verification_otp(user)

    if not verification_otp:
        raise InvalidEmailVerificationOTPException()

    # Check OTP expiry
    if timezone.now() > verification_otp.expires_at:
        raise EmailVerificationOTPExpiredException()

    # Compare entered OTP with hashed OTP
    if not check_password(
        otp,
        verification_otp.otp_hash,
    ):
        # Count only wrong OTP attempts
        verification_otp.verification_attempts += 1

        verification_otp.save(
            update_fields=["verification_attempts"]
        )

        # Maximum 5 wrong attempts
        if verification_otp.verification_attempts >= settings.OTP_MAX_ATTEMPTS:
            delete_email_verification_otps(user)
            raise OTPVerificationAttemptsExceededException()

        raise InvalidEmailVerificationOTPException()

    # OTP is correct
    user.email_verified = True

    user.save(
        update_fields=[
            "email_verified",
            "updated_at",
        ]
    )

    # Delete OTP after successful verification
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
    user = get_user_by_email(email)

    if not user:
        raise InvalidEmailVerificationOTPException()

    if user.email_verified:
        raise EmailAlreadyVerifiedException()

    latest_otp = get_latest_email_verification_otp(user)

    if latest_otp:
        cooldown_end = latest_otp.created_at + timedelta(seconds=settings.OTP_RESEND_COOLDOWN_SECONDS)

        if timezone.now() < cooldown_end:
            raise OTPResendTooSoonException()

    # Delete the previous OTP
    delete_email_verification_otps(user)

    # Generate a new OTP
    otp = generate_otp()

    # Hash OTP before storing
    otp_hash = make_password(otp)

    # OTP expires after 5 minutes
    expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

    create_email_verification_otp(
        user=user,
        otp_hash=otp_hash,
        expires_at=expires_at,
    )

    # Send the raw OTP to the user's email
    send_verification_email(
        email=user.email,
        otp=otp,
    )

    return {
        "message": "A new verification OTP has been sent."
    }


def login_user(validated_data):
    email = validated_data["email"]
    password = validated_data["password"]

    # Find user
    user = get_user_by_email(email)

    # Check credentials and verification status
    if (
        not user
        or not user.check_password(password)
        or not user.email_verified
        or not user.is_active
        or user.is_superuser
    ):
        raise InvalidCredentialsException()

    # Generate JWT tokens
    tokens = generate_tokens_for_user(user)

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
    user = get_verified_user_by_email(email)

    if not user:
        return {
            "message": "If an account exists for this email, a password reset OTP has been sent."
        }

    # Delete any previous password reset OTPs
    delete_password_reset_otps(user)

    # Generate a new OTP
    otp = generate_otp()

    # Hash the OTP before storing it
    otp_hash = make_password(otp)

    # OTP expires after 5 minutes
    expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

    create_password_reset_otp(
        user=user,
        otp_hash=otp_hash,
        expires_at=expires_at,
    )

    # Send the raw OTP to the user's email
    send_password_reset_otp_email(
        email=user.email,
        otp=otp,
    )

    return {
        "message": "If an account exists for this email, a password reset OTP has been sent."
    }


def verify_password_reset_otp(email, otp):
    user = get_verified_user_by_email(email)

    if not user:
        raise InvalidPasswordResetOTPException()

    password_reset_otp = get_latest_password_reset_otp(user)

    if not password_reset_otp:
        raise InvalidPasswordResetOTPException()

    # Check OTP expiry
    if timezone.now() > password_reset_otp.expires_at:
        raise PasswordResetOTPExpiredException()

    # Check OTP
    if not check_password(
        otp,
        password_reset_otp.otp_hash,
    ):
        # Count only wrong attempts
        password_reset_otp.verification_attempts += 1

        password_reset_otp.save(
            update_fields=["verification_attempts"]
        )

        # Maximum 5 wrong attempts
        if password_reset_otp.verification_attempts >= settings.OTP_MAX_ATTEMPTS:
            delete_password_reset_otps(user)

            raise PasswordResetOTPAttemptsExceededException()

        raise InvalidPasswordResetOTPException()

    delete_password_reset_otps(user)

    # Remove any previous reset tokens
    delete_password_reset_tokens(user)

    # Generate new reset token
    raw_token, token_hash = generate_password_reset_token()

    expires_at = timezone.now() + timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRY_MINUTES)

    create_password_reset_token(
        user=user,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    return {
        "message": "OTP verified successfully.",
        "reset_token": raw_token,
    }


def resend_password_reset_otp(email):
    user = get_verified_user_by_email(email)

    if not user:
        raise InvalidCredentialsException()

    latest_otp = get_latest_password_reset_otp(user)

    if latest_otp:
        cooldown_end = latest_otp.created_at + timedelta(seconds=settings.OTP_RESEND_COOLDOWN_SECONDS)

        if timezone.now() < cooldown_end:
            raise OTPResendTooSoonException()

    # Delete previous OTP
    delete_password_reset_otps(user)

    # Generate new OTP
    otp = generate_otp()

    # Hash OTP before storing
    otp_hash = make_password(otp)

    # OTP expires after 5 minutes
    expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

    create_password_reset_otp(
        user=user,
        otp_hash=otp_hash,
        expires_at=expires_at,
    )

    # Send raw OTP to email
    send_password_reset_otp_email(
        email=user.email,
        otp=otp,
    )

    return {
        "message": "A new password reset OTP has been sent."
    }


def generate_password_reset_token():
    raw_token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        raw_token.encode()
    ).hexdigest()

    return raw_token, token_hash


def reset_password(reset_token, new_password):

    token_hash = hashlib.sha256(
        reset_token.encode()
    ).hexdigest()

    token = get_password_reset_token(token_hash)

    if not token:
        raise InvalidPasswordResetTokenException()

    if token.expires_at <= timezone.now():
        raise PasswordResetTokenExpiredException()

    user = token.user

    # Prevent using the current password again
    if user.check_password(new_password):
        raise SamePasswordException()

    user.set_password(new_password)
    user.save(update_fields=["password"])

    # Make token single-use
    token.used_at = timezone.now()
    token.save(update_fields=["used_at"])

    # Remove any other reset tokens
    delete_password_reset_tokens(user)

    return {
        "message": "Password reset successfully."
    }


def google_authenticate(id_token_string):

    try:
        # Verify the ID token sent by the frontend.
        # This checks that the token is valid and was issued
        # for your Google Client ID.
        idinfo = id_token.verify_oauth2_token(
            id_token_string,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )

    except ValueError:
        raise InvalidGoogleTokenException()

    # Get information from the verified Google ID token
    google_id = idinfo.get("sub")
    email = idinfo.get("email")
    email_verified = idinfo.get("email_verified")
    full_name = idinfo.get("name")

    # Basic validation
    if not google_id or not email:
        raise InvalidGoogleTokenException()

    if not email_verified:
        raise InvalidGoogleTokenException()

    # Normalize email
    email = email.lower()

    # ---------------------------------------------------------
    # 1. Check whether this Google account already exists
    # ---------------------------------------------------------

    user = get_user_by_google_id(google_id)

    if user:

        # Google account already linked to this user.
        # Just log them in.
        if not user.is_active:
            raise InvalidGoogleTokenException()

    else:

        # ---------------------------------------------------------
        # 2. Google account does not exist yet.
        #    Check whether the email already belongs to a user.
        # ---------------------------------------------------------

        user = get_verified_user_by_email(email)

        if user:

            # -------------------------------------------------
            # Existing normal email/password account
            # -------------------------------------------------
            #
            # Link this Google account to the existing user.
            #
            # Example:
            #
            # Before:
            # email = john@gmail.com
            # google_id = None
            #
            # After:
            # email = john@gmail.com
            # google_id = 123456789
            #

            if user.google_id and user.google_id != google_id:
                # This email is already linked to a different
                # Google account.
                raise InvalidGoogleTokenException()

            user.google_id = google_id
            user.save(update_fields=["google_id"])

        else:

            # -------------------------------------------------
            # 3. Completely new user
            # -------------------------------------------------

            user = create_google_user(
                full_name=full_name or email.split("@")[0],
                email=email,
                google_id=google_id,
            )

    # ---------------------------------------------------------
    # 4. Check whether the account is active
    # ---------------------------------------------------------

    if not user.is_active:
        raise InvalidGoogleTokenException()

    # ---------------------------------------------------------
    # 5. Generate your application's JWT tokens
    # ---------------------------------------------------------

    tokens = generate_tokens_for_user(user)

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

    user = get_user_by_email(email)

    if (
        not user
        or not user.check_password(password)
        or not user.is_active
        or not user.is_staff
        or not user.is_superuser
    ):
        raise InvalidCredentialsException()

    tokens = generate_tokens_for_user(user)

    return {
        "message": "Admin login successful.",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        },
        "tokens": tokens,
    }
