import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdmin
from apps.admins.serializers.instructor_serializer import (
    InstructorDetailSerializer,
    InstructorListSerializer,
)
from apps.admins.services.instructor_service import InstructorService

logger = logging.getLogger(__name__)


class AdminInstructorListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        logger.info(
            "Admin requested instructor list.",
            extra={"user_id": request.user.id},
        )

        instructors = InstructorService.get_instructors()

        serializer = InstructorListSerializer(
            instructors,
            many=True,
            context={"request": request},
        )

        logger.info(
            "Instructor list returned successfully.",
            extra={
                "user_id": request.user.id,
                "count": len(serializer.data),
            },
        )

        return Response(serializer.data)


class AdminInstructorDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, instructor_id):
        logger.info(
            "Admin requested instructor detail.",
            extra={
                "user_id": request.user.id,
                "instructor_id": instructor_id,
            },
        )

        instructor = InstructorService.get_instructor(instructor_id)

        serializer = InstructorDetailSerializer(
            instructor,
            context={"request": request},
        )

        logger.info(
            "Instructor detail returned successfully.",
            extra={
                "user_id": request.user.id,
                "instructor_id": instructor_id,
            },
        )

        return Response(serializer.data)
