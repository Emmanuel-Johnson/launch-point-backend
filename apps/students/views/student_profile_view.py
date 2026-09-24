from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.students.serializers.student_profile_serializer import (
    StudentProfileSerializer,
)
from apps.students.services.student_profile_service import (
    StudentProfileService,
)


class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = StudentProfileService.get_profile(
            user=request.user,
        )

        serializer = StudentProfileSerializer(profile)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        profile = StudentProfileService.update_profile(
            user=request.user,
            data=request.data,
        )

        serializer = StudentProfileSerializer(profile)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
