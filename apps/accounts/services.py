from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)
from .repositories import (
    create_user,
    get_user_by_email,
    create_email_verification_otp,
    delete_email_verification_otps,
)
from .utils import generate_otp, send_verification_email


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

    # Set OTP expiry time
    expires_at = timezone.now() + timedelta(minutes=10)

    # Store the hashed OTP
    create_email_verification_otp(
        user=user,
        otp_hash=otp_hash,
        expires_at=expires_at,
    )

    # Send OTP to user's email
    send_verification_email(
        user.email,
        otp,
    )

    return {
        "message": "Account created successfully. Please verify your email.",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        },
    }


def login_user(validated_data):
    email = validated_data["email"]
    password = validated_data["password"]

    # Find user by email
    user = get_user_by_email(email)

    # Check credentials
    if not user or not user.check_password(password):
        raise InvalidCredentialsException()

    return {
        "message": "Login successful.",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        },
    }
