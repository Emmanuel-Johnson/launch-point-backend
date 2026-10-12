import logging

from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.instructors.serializers.instructor_profile_serializer import (
    InstructorProfileSerializer,
    InstructorProfileUpdateSerializer,
)
from apps.instructors.services.instructor_profile_service import (
    InstructorProfileService,
)

logger = logging.getLogger(__name__)


class InstructorProfileView(APIView):
    """Retrieve and update the authenticated instructor's profile."""

    permission_classes = [IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser,
        JSONParser,
    ]

    def get(self, request):
        """Retrieve the instructor's profile."""

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

    def patch(self, request):
        """Partially update the instructor's profile."""

        logger.info(
            "Instructor requested profile update.",
            extra={"user_id": request.user.id},
        )

        # Confirm that the authenticated user has an instructor profile.
        InstructorProfileService.get_profile(user=request.user)

        serializer = InstructorProfileUpdateSerializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        profile = InstructorProfileService.update_profile(
            user=request.user,
            data=serializer.validated_data,
        )

        # Return the same response format as the GET endpoint.
        response_serializer = InstructorProfileSerializer(profile)

        logger.info(
            "Instructor profile updated successfully.",
            extra={"user_id": request.user.id},
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
