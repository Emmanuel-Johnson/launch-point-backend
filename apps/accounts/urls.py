from django.urls import path

from .views import (
    SignupView,
    VerifyEmailOTPView,
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
]