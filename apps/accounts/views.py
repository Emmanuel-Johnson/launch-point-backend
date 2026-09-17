from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .permissions import IsAdminUser
from .serializers import (
    SignupSerializer,
    VerifyEmailOTPSerializer,
    LoginSerializer,
    ResendEmailVerificationOTPSerializer,
    ForgotPasswordSerializer,
    VerifyPasswordResetOTPSerializer,
    ResendPasswordResetOTPSerializer,
    ResetPasswordSerializer,
    GoogleAuthenticationSerializer,
    AdminLoginSerializer,
)
from .services import (
    signup_user,
    verify_email_otp,
    login_user,
    resend_verification_otp,
    forgot_password,
    verify_password_reset_otp,
    resend_password_reset_otp,
    reset_password,
    google_authenticate,
    admin_login_user,
)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = signup_user(
            serializer.validated_data
        )

        return Response(
            result,
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyEmailOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

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
        serializer = ResendEmailVerificationOTPSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        result = resend_verification_otp(
            email=serializer.validated_data["email"]
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = login_user(
            serializer.validated_data
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = forgot_password(
            email=serializer.validated_data["email"]
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class VerifyPasswordResetOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyPasswordResetOTPSerializer(
            data=request.data
        )

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
        serializer = ResendPasswordResetOTPSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        result = resend_password_reset_otp(
            email=serializer.validated_data["email"]
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = reset_password(
            reset_token=serializer.validated_data[
                "reset_token"
            ],
            new_password=serializer.validated_data[
                "new_password"
            ],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class GoogleAuthenticationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = GoogleAuthenticationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = google_authenticate(
            serializer.validated_data["id_token"]
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {
                    "detail": "Refresh token is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)

            token.blacklist()

        except TokenError:
            return Response(
                {
                    "detail": "Invalid or expired refresh token."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {
                "message": "Logout successful."
            },
            status=status.HTTP_200_OK,
        )


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = admin_login_user(
            serializer.validated_data
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class AdminLogoutView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        refresh_token = request.data.get("admin_refresh")

        if not refresh_token:
            return Response(
                {
                    "detail": "Refresh token is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except TokenError:
            return Response(
                {
                    "detail": "Invalid or expired refresh token."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {
                "message": "Admin logout successful."
            },
            status=status.HTTP_200_OK,
        )
