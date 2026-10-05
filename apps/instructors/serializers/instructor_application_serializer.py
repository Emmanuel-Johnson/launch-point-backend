from rest_framework import serializers


class InstructorApplicationFormSerializer(serializers.Serializer):
    full_name = serializers.CharField(
        read_only=True,
    )

    email = serializers.EmailField(
        read_only=True,
    )

    profile_image = serializers.ImageField(
        read_only=True,
        allow_null=True,
    )

    location = serializers.CharField(
        read_only=True,
        allow_blank=True,
        source="student_profile.location",
    )

    education = serializers.CharField(
        read_only=True,
        allow_blank=True,
        source="student_profile.education",
    )

    occupation = serializers.CharField(
        read_only=True,
        allow_blank=True,
        source="student_profile.occupation",
    )

    github_url = serializers.URLField(
        read_only=True,
        allow_blank=True,
        source="student_profile.github_url",
    )

    linkedin_url = serializers.URLField(
        read_only=True,
        allow_blank=True,
        source="student_profile.linkedin_url",
    )

    portfolio_url = serializers.URLField(
        read_only=True,
        allow_blank=True,
        source="student_profile.portfolio_url",
    )
