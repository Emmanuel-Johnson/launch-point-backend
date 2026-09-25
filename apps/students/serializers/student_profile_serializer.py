from rest_framework import serializers

from apps.students.models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="user.full_name",
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "full_name",
            "email",
            "profile_image",
            "bio",
            "location",
            "education",
            "occupation",
            "github_url",
            "linkedin_url",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "email",
            "created_at",
            "updated_at",
        ]

    def validate_bio(self, value):
        value = value.strip()

        if len(value) > 500:
            raise serializers.ValidationError("Bio cannot exceed 500 characters.")

        return value

    def validate_location(self, value):
        return value.strip()

    def validate_education(self, value):
        return value.strip()

    def validate_occupation(self, value):
        return value.strip()

    def validate_github_url(self, value):
        return value.strip()

    def validate_linkedin_url(self, value):
        return value.strip()
