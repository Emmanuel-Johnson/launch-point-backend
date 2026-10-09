from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.admins.serializers.instructor_application_serializer import (
    AdminInstructorApplicationListSerializer,
)
from apps.admins.services.instructor_application_service import (
    InstructorApplicationService,
)


class AdminInstructorApplicationListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        applications = InstructorApplicationService.get_all_applications()

        serializer = AdminInstructorApplicationListSerializer(
            applications,
            many=True,
        )

        return Response(serializer.data)
