from rest_framework.throttling import AnonRateThrottle


class SignupRateThrottle(AnonRateThrottle):
    scope = "signup"
    message = "Too many signup attempts. Please try again later."


class OTPRateThrottle(AnonRateThrottle):
    scope = "otp"
    message = "Too many OTP attempts. Please try again later."


class LoginRateThrottle(AnonRateThrottle):
    scope = "login"
    message = "Too many login attempts. Please try again later."


class PasswordResetRateThrottle(AnonRateThrottle):
    scope = "password_reset"
    message = "Too many password reset attempts. Please try again later."


class GoogleAuthRateThrottle(AnonRateThrottle):
    scope = "google_auth"
    message = "Too many Google authentication attempts. Please try again later."


class AdminLoginRateThrottle(AnonRateThrottle):
    scope = "admin_login"
    message = "Too many admin login attempts. Please try again later."
