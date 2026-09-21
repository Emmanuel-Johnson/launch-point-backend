from rest_framework.throttling import AnonRateThrottle


class SignupRateThrottle(AnonRateThrottle):
    scope = "signup"


class OTPRateThrottle(AnonRateThrottle):
    scope = "otp"


class LoginRateThrottle(AnonRateThrottle):
    scope = "login"


class PasswordResetRateThrottle(AnonRateThrottle):
    scope = "password_reset"


class GoogleAuthRateThrottle(AnonRateThrottle):
    scope = "google_auth"


class AdminLoginRateThrottle(AnonRateThrottle):
    scope = "admin_login"
