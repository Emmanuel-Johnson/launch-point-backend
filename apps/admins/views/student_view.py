import logging

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.admins.serializers.student_serializer import (
    StudentDetailSerializer,
    StudentListSerializer,
    StudentStatusSerializer,
)
from apps.admins.services.student_service import StudentService

logger = logging.getLogger(__name__)


class AdminStudentListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logger.info(
            "Admin requested student list.",
            extra={"user_id": request.user.id},
        )

        students = StudentService.get_students()

        serializer = StudentListSerializer(
            students,
            many=True,
        )

        logger.info(
            "Student list returned successfully.",
            extra={"user_id": request.user.id, "count": len(serializer.data)},
        )

        return Response(serializer.data)


class AdminStudentDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, student_id):
        logger.info(
            "Admin requested student detail.",
            extra={"user_id": request.user.id, "student_id": student_id},
        )

        student = StudentService.get_student(student_id)

        serializer = StudentDetailSerializer(student)

        logger.info(
            "Student detail returned successfully.",
            extra={"user_id": request.user.id, "student_id": student_id},
        )

        return Response(serializer.data)


class AdminStudentStatusView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, student_id):
        logger.info(
            "Admin requested student status update.",
            extra={"user_id": request.user.id, "student_id": student_id},
        )

        is_active = request.data.get("is_active")

        if not isinstance(is_active, bool):
            logger.warning(
                "Student status update rejected: is_active must be a boolean.",
                extra={"user_id": request.user.id, "student_id": student_id},
            )
            return Response(
                {"detail": "is_active must be a boolean."},
                status=400,
            )

        student = StudentService.update_student_status(
            student_id=student_id,
            is_active=is_active,
        )

        serializer = StudentStatusSerializer(student)

        message = (
            "Student activated successfully."
            if student.is_active
            else "Student deactivated successfully."
        )

        logger.info(
            "Student status updated successfully.",
            extra={
                "user_id": request.user.id,
                "student_id": student_id,
                "is_active": student.is_active,
            },
        )

        return Response(
            {
                **serializer.data,
                "message": message,
            }
        )
