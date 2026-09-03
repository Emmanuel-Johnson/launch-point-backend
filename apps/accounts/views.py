from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import (
    SignupSerializer,
    VerifyEmailOTPSerializer,
    LoginSerializer,
)

from .services import (
    signup_user,
    verify_email_otp,
    login_user,
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
