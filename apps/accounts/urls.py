from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    SignupView,
    VerifyEmailOTPView,
    LoginView,
    LogoutView,
    ResendEmailVerificationOTPView,
    ForgotPasswordView,
    VerifyPasswordResetOTPView,
)


urlpatterns = [

    path(
        "signup/",
        SignupView.as_view(),
        name="signup",
    ),

    path(
        "verify-email/",
        VerifyEmailOTPView.as_view(),
        name="verify-email",
    ),

    path(
        "resend-verification-otp/",
        ResendEmailVerificationOTPView.as_view(),
        name="resend-verification-otp",
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "forgot-password/",
        ForgotPasswordView.as_view(),
        name="forgot-password",
    ),

    path(
        "verify-password-reset-otp/",
        VerifyPasswordResetOTPView.as_view(),
        name="verify-password-reset-otp",
    ),

    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]
