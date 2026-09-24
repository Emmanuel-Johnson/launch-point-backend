from rest_framework import serializers

from apps.students.models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="user.full_name",
        read_only=True,
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
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "full_name",
            "email",
            "created_at",
            "updated_at",
        ]
