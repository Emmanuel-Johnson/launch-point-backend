from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.instructors.serializers.instructor_application_serializer import (
    InstructorApplicationCreateSerializer,
    InstructorApplicationDetailSerializer,
    InstructorApplicationFormSerializer,
    InstructorApplicationListSerializer,
)
from apps.instructors.services.instructor_application_service import (
    InstructorApplicationService,
)


class InstructorApplicationFormView(APIView):
    """API view for instructor application form data."""

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        data = InstructorApplicationService.get_application_form_data(
            user=request.user,
        )

        serializer = InstructorApplicationFormSerializer(data)

        return Response(serializer.data)

    def post(self, request):
        serializer = InstructorApplicationCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        supporting_files = request.FILES.getlist(
            "supporting_files",
        )

        application = InstructorApplicationService.submit_application(
            user=request.user,
            validated_data=serializer.validated_data,
            supporting_files=supporting_files,
        )

        return Response(
            {
                "message": "Your instructor application has been submitted "
                "successfully.",
                "id": application.id,
                "status": application.status,
                "submitted_at": application.submitted_at,
            },
            status=201,
        )


class InstructorApplicationListView(APIView):
    """API view for the current user's instructor applications."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        applications = InstructorApplicationService.get_user_applications(
            user=request.user
        )

        serializer = InstructorApplicationListSerializer(
            applications,
            many=True,
        )

        return Response(serializer.data)


class InstructorApplicationDetailView(APIView):
    """API view for a single instructor application."""

    permission_classes = [IsAuthenticated]

    def get(self, request, application_id):
        application = InstructorApplicationService.get_user_application_detail(
            user=request.user,
            application_id=application_id,
        )

        serializer = InstructorApplicationDetailSerializer(
            application,
            context={"request": request},
        )

        return Response(serializer.data)
