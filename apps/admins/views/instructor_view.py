import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdmin
from apps.admins.serializers.instructor_serializer import (
    InstructorDetailSerializer,
    InstructorListSerializer,
    InstructorStatusSerializer,
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


class AdminInstructorStatusView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, instructor_id):
        serializer = InstructorStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_active = serializer.validated_data["is_active"]

        instructor = InstructorService.update_instructor_status(
            instructor_id=instructor_id,
            is_active=is_active,
        )

        return Response(
            {
                "message": (
                    "Instructor activated successfully."
                    if is_active
                    else "Instructor deactivated successfully."
                ),
                "id": instructor.id,
                "is_active": instructor.is_active,
            },
            status=status.HTTP_200_OK,
        )
