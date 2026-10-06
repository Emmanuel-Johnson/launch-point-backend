from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.instructors.serializers.instructor_application_serializer import (
    InstructorApplicationFormSerializer,
)
from apps.instructors.services.instructor_application_service import (
    InstructorApplicationService,
)


class InstructorApplicationFormView(APIView):
    """API view for instructor application form data."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = InstructorApplicationService.get_application_form_data(
            user=request.user,
        )

        serializer = InstructorApplicationFormSerializer(data)

        return Response(serializer.data)
