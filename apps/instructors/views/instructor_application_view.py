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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = InstructorApplicationService.get_application_form_data(user=request.user)

        serializer = InstructorApplicationFormSerializer(user)

        return Response(serializer.data)
