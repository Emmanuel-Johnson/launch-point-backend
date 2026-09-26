from rest_framework import serializers

from apps.accounts.models import User


class StudentListSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(
        source="student_profile.profile_image",
        read_only=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "profile_image",
            "date_joined",
            "is_active",
        ]


class StudentDetailSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(
        source="student_profile.profile_image",
        read_only=True,
    )

    bio = serializers.CharField(
        source="student_profile.bio",
        read_only=True,
    )

    location = serializers.CharField(
        source="student_profile.location",
        read_only=True,
    )

    education = serializers.CharField(
        source="student_profile.education",
        read_only=True,
    )

    occupation = serializers.CharField(
        source="student_profile.occupation",
        read_only=True,
    )

    github_url = serializers.URLField(
        source="student_profile.github_url",
        read_only=True,
    )

    linkedin_url = serializers.URLField(
        source="student_profile.linkedin_url",
        read_only=True,
    )

    portfolio_url = serializers.URLField(
        source="student_profile.portfolio_url",
        read_only=True,
    )

    profile_created_at = serializers.DateTimeField(
        source="student_profile.created_at",
        read_only=True,
    )

    profile_updated_at = serializers.DateTimeField(
        source="student_profile.updated_at",
        read_only=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "role",
            "profile_image",
            "bio",
            "location",
            "education",
            "occupation",
            "github_url",
            "linkedin_url",
            "portfolio_url",
            "email_verified",
            "is_active",
            "date_joined",
            "updated_at",
            "profile_created_at",
            "profile_updated_at",
        ]
