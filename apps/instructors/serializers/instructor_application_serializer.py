from rest_framework import serializers

from apps.categories.models import Category
from apps.instructors.models import InstructorApplication


class InstructorApplicationUserSerializer(serializers.Serializer):
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


class InstructorApplicationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class InstructorApplicationFormSerializer(serializers.Serializer):
    user = InstructorApplicationUserSerializer(
        read_only=True,
    )

    categories = InstructorApplicationCategorySerializer(
        many=True,
        read_only=True,
    )


class InstructorApplicationCreateSerializer(serializers.ModelSerializer):
    categories_to_teach = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.filter(is_active=True),
        required=True,
    )

    class Meta:
        model = InstructorApplication
        fields = (
            "full_name",
            "profile_image",
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
        )

    def validate_categories_to_teach(self, categories):
        if not categories:
            raise serializers.ValidationError("Select at least one category.")

        if len(categories) > 10:
            raise serializers.ValidationError("You can select up to 10 categories.")

        return categories

    def validate_terms_accepted(self, value):
        if not value:
            raise serializers.ValidationError(
                "You must accept the terms before submitting."
            )

        return value
