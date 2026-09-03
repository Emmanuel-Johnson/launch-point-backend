from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    SignupSerializer,
    VerifyEmailOTPSerializer,
)
from .services import (
    signup_user,
    verify_email_otp,
)


class SignupView(APIView):

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

    def post(self, request):
        print(request.data)
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
