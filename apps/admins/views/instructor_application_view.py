from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.admins.serializers.instructor_application_serializer import (
    AdminInstructorApplicationDetailSerializer,
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
            context={"request": request},
        )

        return Response(serializer.data)


class AdminInstructorApplicationDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, application_id):
        application = InstructorApplicationService.get_application_by_id(application_id)

        if application is None:
            raise NotFound("Instructor application not found.")

        serializer = AdminInstructorApplicationDetailSerializer(
            application,
            context={"request": request},
        )

        return Response(serializer.data)
