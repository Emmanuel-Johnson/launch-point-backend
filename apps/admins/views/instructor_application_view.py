from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdmin
from apps.admins.serializers.instructor_application_serializer import (
    AdminInstructorApplicationApproveSerializer,
    AdminInstructorApplicationDetailSerializer,
    AdminInstructorApplicationListSerializer,
    AdminInstructorApplicationRejectSerializer,
)
from apps.admins.services.instructor_application_service import (
    InstructorApplicationService,
)


class AdminInstructorApplicationListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        applications = InstructorApplicationService.get_all_applications()

        serializer = AdminInstructorApplicationListSerializer(
            applications,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)


class AdminInstructorApplicationDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, application_id):
        application = InstructorApplicationService.get_application_by_id(application_id)

        if application is None:
            raise NotFound("Instructor application not found.")

        serializer = AdminInstructorApplicationDetailSerializer(
            application,
            context={"request": request},
        )

        return Response(serializer.data)


class AdminInstructorApplicationRejectView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, application_id):
        request_serializer = AdminInstructorApplicationRejectSerializer(
            data=request.data
        )
        request_serializer.is_valid(raise_exception=True)

        application = InstructorApplicationService.reject_application(
            application_id=application_id,
            admin=request.user,
            admin_message=request_serializer.validated_data["admin_message"],
        )

        return Response(
            {
                "message": "Application rejected successfully.",
                "status": application.status,
                "admin_message": application.admin_message,
                "reviewed_at": application.reviewed_at,
            }
        )


class AdminInstructorApplicationApproveView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, application_id):
        request_serializer = AdminInstructorApplicationApproveSerializer(
            data=request.data
        )
        request_serializer.is_valid(raise_exception=True)

        application = InstructorApplicationService.approve_application(
            application_id=application_id,
            admin=request.user,
            admin_message=request_serializer.validated_data["admin_message"],
        )

        return Response(
            {
                "message": "Application approved successfully.",
                "status": application.status,
                "admin_message": application.admin_message,
                "reviewed_at": application.reviewed_at,
            }
        )
