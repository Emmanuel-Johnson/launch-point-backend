import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.instructors.serializers.instructor_profile_serializer import (
    InstructorProfileSerializer,
)
from apps.instructors.services.instructor_profile_service import (
    InstructorProfileService,
)

logger = logging.getLogger(__name__)


class InstructorProfileView(APIView):
    """
    API view for retrieving the authenticated instructor's profile.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the authenticated instructor's profile.
        """

        logger.info(
            "Instructor requested profile retrieval.",
            extra={"user_id": request.user.id},
        )

        profile = InstructorProfileService.get_profile(
            user=request.user,
        )

        serializer = InstructorProfileSerializer(profile)

        logger.info(
            "Instructor profile retrieved successfully.",
            extra={"user_id": request.user.id},
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
