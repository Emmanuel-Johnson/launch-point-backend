from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.permissions import IsStudentOrInstructor
from apps.instructors.models import InstructorProfile


class SwitchToInstructorView(APIView):
    permission_classes = [IsAuthenticated, IsStudentOrInstructor]

    def post(self, request):
        user = request.user

        # Check whether the user's role is student.
        if user.role == User.Role.STUDENT:
            return Response(
                {
                    "message": (
                        "Your instructor account has been deactivated. "
                        "Please contact Launch Point Support for assistance."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Verify the user has an approved instructor application.
        has_approved_application = user.instructor_applications.filter(
            status="approved"
        ).exists()

        if not has_approved_application:
            return Response(
                {"detail": "You are not approved to switch to instructor."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get the instructor profile.
        try:
            instructor_profile = user.instructor_profile
        except InstructorProfile.DoesNotExist:
            return Response(
                {"detail": "Instructor profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get the instructor profile image URL.
        profile_image = (
            request.build_absolute_uri(instructor_profile.profile_image.url)
            if instructor_profile.profile_image
            else None
        )

        return Response(
            {
                "message": (
                    "Switched to your Instructor Dashboard! "
                    "Start sharing your knowledge and inspiring learners."
                ),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": instructor_profile.full_name,
                    "profile_image": profile_image,
                    "role": User.Role.INSTRUCTOR,
                },
            },
            status=status.HTTP_200_OK,
        )
