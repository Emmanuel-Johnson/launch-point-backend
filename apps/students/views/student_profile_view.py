import logging

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.students.serializers.student_profile_serializer import (
    StudentProfileSerializer,
)
from apps.students.services.student_profile_service import (
    StudentProfileService,
)

logger = logging.getLogger(__name__)


class StudentProfileView(APIView):
    """
    API view for retrieving and updating the authenticated
    student's profile.
    """

    permission_classes = [IsAuthenticated]

    parser_classes = [
        MultiPartParser,
    ]

    def get(self, request):
        """
        Retrieve the authenticated student's profile.
        """

        logger.info(
            "Student requested profile retrieval.",
            extra={"user_id": request.user.id},
        )

        profile = StudentProfileService.get_profile(
            user=request.user,
        )

        serializer = StudentProfileSerializer(
            profile,
        )

        logger.info(
            "Student profile retrieved successfully.",
            extra={"user_id": request.user.id},
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        """
        Partially update the authenticated student's profile.
        """

        logger.info(
            "Student requested profile update.",
            extra={"user_id": request.user.id},
        )

        serializer = StudentProfileSerializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        profile = StudentProfileService.update_profile(
            user=request.user,
            data=serializer.validated_data,
        )

        response_serializer = StudentProfileSerializer(
            profile,
        )

        logger.info(
            "Student profile updated successfully.",
            extra={"user_id": request.user.id},
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
