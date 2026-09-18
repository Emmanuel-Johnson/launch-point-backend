import logging

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdminUser
from .serializers import (
    AdminLoginSerializer,
    ForgotPasswordSerializer,
    GoogleAuthenticationSerializer,
    LoginSerializer,
    ResendEmailVerificationOTPSerializer,
    ResendPasswordResetOTPSerializer,
    ResetPasswordSerializer,
    SignupSerializer,
    VerifyEmailOTPSerializer,
    VerifyPasswordResetOTPSerializer,
)
from .services import (
    admin_login_user,
    forgot_password,
    google_authenticate,
    login_user,
    resend_password_reset_otp,
    resend_verification_otp,
    reset_password,
    signup_user,
    verify_email_otp,
    verify_password_reset_otp,
)

logger = logging.getLogger(__name__)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Signup request received")

        serializer = SignupSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        result = signup_user(serializer.validated_data)

        return Response(
            result,
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Email verification request received")

        serializer = VerifyEmailOTPSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        result = verify_email_otp(
            email=serializer.validated_data["email"],
            otp=serializer.validated_data["otp"],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class ResendEmailVerificationOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Verification OTP resend request received")

        serializer = ResendEmailVerificationOTPSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        result = resend_verification_otp(email=serializer.validated_data["email"])

        return Response(result, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Login request received")

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        result = login_user(serializer.validated_data)

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Forgot password request received")

        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = forgot_password(email=serializer.validated_data["email"])

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class VerifyPasswordResetOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Password reset OTP verification request received")

        serializer = VerifyPasswordResetOTPSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        result = verify_password_reset_otp(
            email=serializer.validated_data["email"],
            otp=serializer.validated_data["otp"],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class ResendPasswordResetOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Password reset OTP resend request received")

        serializer = ResendPasswordResetOTPSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        result = resend_password_reset_otp(email=serializer.validated_data["email"])

        return Response(result, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Reset password request received")

        serializer = ResetPasswordSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        result = reset_password(
            reset_token=serializer.validated_data["reset_token"],
            new_password=serializer.validated_data["new_password"],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class GoogleAuthenticationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Google authentication request received")

        serializer = GoogleAuthenticationSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        result = google_authenticate(serializer.validated_data["id_token"])

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info("Logout request received user_id=%s", request.user.id)

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            logger.warning(
                "Logout failed: refresh token missing user_id=%s",
                request.user.id,
            )
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)

            token.blacklist()

        except TokenError:
            logger.warning(
                "Logout failed: invalid or expired refresh token user_id=%s",
                request.user.id,
            )
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        logger.info("Logout successful user_id=%s", request.user.id)

        return Response(
            {"message": "Logout successful."},
            status=status.HTTP_200_OK,
        )


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Admin login request received")

        serializer = AdminLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        result = admin_login_user(serializer.validated_data)

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class AdminLogoutView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        logger.info("Admin logout request received user_id=%s", request.user.id)

        refresh_token = request.data.get("admin_refresh")

        if not refresh_token:
            logger.warning(
                "Admin logout failed: refresh token missing user_id=%s",
                request.user.id,
            )
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except TokenError:
            logger.warning(
                "Admin logout failed: invalid or expired refresh token user_id=%s",
                request.user.id,
            )
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        logger.info("Admin logout successful user_id=%s", request.user.id)

        return Response(
            {"message": "Admin logout successful."},
            status=status.HTTP_200_OK,
        )
