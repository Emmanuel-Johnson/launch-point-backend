from datetime import timedelta
from django.contrib.auth.hashers import (
    check_password,
    make_password,
)
from django.utils import timezone
from .exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    InvalidEmailVerificationOTPException,
    EmailVerificationOTPExpiredException,
    EmailAlreadyVerifiedException,
    EmailNotVerifiedException,
)
from .repositories import (
    create_user,
    get_user_by_email,
    create_email_verification_otp,
    get_latest_email_verification_otp,
    delete_email_verification_otps,
)
from .utils import (
    generate_otp,
    send_verification_email,
)
from rest_framework_simplejwt.tokens import RefreshToken


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

    if existing_user:
        raise EmailAlreadyExistsException()

    # Create the user
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

    # OTP expires after 10 minutes
    expires_at = timezone.now() + timedelta(minutes=10)

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


def login_user(validated_data):
    email = validated_data["email"]
    password = validated_data["password"]

    # Find user
    user = get_user_by_email(email)

    # Check credentials
    if not user or not user.check_password(password):
        raise InvalidCredentialsException()

    # Email must be verified
    if not user.email_verified:
        raise EmailNotVerifiedException()

    # User must be active
    if not user.is_active:
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
