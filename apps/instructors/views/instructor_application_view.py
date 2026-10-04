from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from apps.instructors.serializers.instructor_application_serializer import (
    InstructorApplicationSerializer,
)


class InstructorApplicationCreateView(generics.CreateAPIView):
    serializer_class = InstructorApplicationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
