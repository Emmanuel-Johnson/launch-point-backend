from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    SignupView,
    VerifyEmailOTPView,
    LoginView,
    LogoutView,
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
        "login/",
        LoginView.as_view(),
        name="login",
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
