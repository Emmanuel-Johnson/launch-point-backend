from pathlib import Path

from rest_framework import serializers

from apps.instructors.models import InstructorApplication
from apps.instructors.services.instructor_application_service import (
    InstructorApplicationService,
)


class InstructorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorApplication
        fields = [
            "id",
            "occupation",
            "education",
            "years_of_experience",
            "categories_to_teach",
            "short_bio",
            "phone_number",
            "location",
            "linkedin_url",
            "github_url",
            "portfolio_url",
            "motivation",
            "resume",
            "terms_accepted",
            "status",
            "admin_message",
            "submitted_at",
            "reviewed_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "admin_message",
            "submitted_at",
            "reviewed_at",
            "updated_at",
        ]

    def validate_terms_accepted(self, value):
        if not value:
            raise serializers.ValidationError(
                "You must accept the terms and conditions."
            )
        return value

    def validate_categories_to_teach(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Categories to teach must be a list.")

        if any(not isinstance(topic, str) or not topic.strip() for topic in value):
            raise serializers.ValidationError("Each topic must be a non-empty string.")

        if len(value) > 10:
            raise serializers.ValidationError(
                "You can select a maximum of 10 categories."
            )

        return [topic.strip() for topic in value]

    def validate_resume(self, value):
        allowed_extensions = {".pdf", ".doc", ".docx"}
        extension = Path(value.name).suffix.lower()

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Upload your resume as a PDF, DOC, or DOCX file."
            )

        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Resume size must not exceed 5 MB.")

        return value

    def create(self, validated_data):
        request = self.context["request"]

        return InstructorApplicationService.create_application(
            user=request.user,
            application_data=validated_data,
        )
