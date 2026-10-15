from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.permissions import IsInstructor


class SwitchToStudentView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]

    def post(self, request):

        user = request.user

        # Get the profile image URL.
        profile_image = (
            request.build_absolute_uri(user.profile_image.url)
            if user.profile_image
            else None
        )

        return Response(
            {
                "message": (
                    "Switched to your Student Dashboard. Keep learning and growing!"
                ),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "profile_image": profile_image,
                    "role": User.Role.STUDENT,
                },
            },
            status=status.HTTP_200_OK,
        )
