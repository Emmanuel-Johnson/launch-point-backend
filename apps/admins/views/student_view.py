from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.admins.serializers.student_serializer import (
    StudentDetailSerializer,
    StudentListSerializer,
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
