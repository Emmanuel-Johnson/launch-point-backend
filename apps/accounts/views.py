from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    SignupSerializer,
    VerifyEmailOTPSerializer,
)
from .services import signup_user


class SignupView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        result = signup_user(
            serializer.validated_data
        )

        return Response(
            result,
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailOTPView(APIView):

    def post(self, request):
        serializer = VerifyEmailOTPSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        # OTP verification service will be added next.

        return Response(
            {
                "message": "OTP data is valid."
            },
            status=status.HTTP_200_OK,
        )