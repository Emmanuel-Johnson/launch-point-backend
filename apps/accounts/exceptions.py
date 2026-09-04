from rest_framework import status
from rest_framework.exceptions import APIException


class EmailAlreadyExistsException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "An account with this email already exists."
    default_code = "email_already_exists"


class EmailNotVerifiedException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Please verify your email before logging in."
    default_code = "email_not_verified"


class InvalidCredentialsException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid email or password."
    default_code = "invalid_credentials"


class InvalidEmailVerificationOTPException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid email verification OTP."
    default_code = "invalid_email_verification_otp"


class EmailVerificationOTPExpiredException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Email verification OTP has expired."
    default_code = "email_verification_otp_expired"


class EmailAlreadyVerifiedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Email is already verified."
    default_code = "email_already_verified"


class OTPResendTooSoonException(APIException):
    status_code = 429
    default_detail = "Please wait before requesting another OTP."


class InvalidPasswordResetOTPException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid password reset OTP."
    default_code = "invalid_password_reset_otp"


class PasswordResetOTPExpiredException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Password reset OTP has expired."
    default_code = "password_reset_otp_expired"
