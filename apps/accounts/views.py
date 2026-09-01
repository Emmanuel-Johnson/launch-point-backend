from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    SignupSerializer,
    VerifyEmailSerializer,
    LoginSerializer,
)


class SignupView(APIView):

    def post(self, request):
        serializer = SignupSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(
            {
                "message": "Verification code sent to your email.",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailView(APIView):

    def post(self, request):
        serializer = VerifyEmailSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(
            {
                "message": "Email verified successfully.",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        return Response(
            {
                "message": "Login successful.",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )