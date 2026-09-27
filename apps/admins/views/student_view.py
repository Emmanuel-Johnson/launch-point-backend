from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.admins.serializers.student_serializer import (
    StudentDetailSerializer,
    StudentListSerializer,
    StudentStatusSerializer,
)
from apps.admins.services.student_service import StudentService


class AdminStudentListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        students = StudentService.get_students()

        serializer = StudentListSerializer(
            students,
            many=True,
        )

        return Response(serializer.data)


class AdminStudentDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, student_id):
        student = StudentService.get_student(student_id)

        serializer = StudentDetailSerializer(student)

        return Response(serializer.data)


class AdminStudentStatusView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, student_id):
        is_active = request.data.get("is_active")

        if not isinstance(is_active, bool):
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

        return Response(
            {
                **serializer.data,
                "message": message,
            }
        )
