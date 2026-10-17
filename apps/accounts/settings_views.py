from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsStudentOrInstructor
from apps.accounts.settings_serializers import ChangePasswordSerializer
from apps.accounts.settings_services import SettingsService


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, IsStudentOrInstructor]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        SettingsService.change_password(
            user=request.user,
            new_password=serializer.validated_data["new_password"],
        )

        return Response(
            {
                "message": "Password updated successfully. "
                "Please sign in with your new password."
            },
            status=status.HTTP_200_OK,
        )
