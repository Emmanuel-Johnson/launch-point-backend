from rest_framework import serializers

from apps.instructors.models import InstructorProfile


class InstructorListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    profile_image = serializers.ImageField(read_only=True)

    experience_years = serializers.IntegerField(read_only=True)
    experience_months = serializers.IntegerField(read_only=True)

    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
        source="categories_to_teach",
    )

    class Meta:
        model = InstructorProfile
        fields = [
            "id",
            "full_name",
            "email",
            "is_active",
            "profile_image",
            "occupation",
            "location",
            "experience_years",
            "experience_months",
            "categories",
            "became_instructor_at",
        ]


class InstructorDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    profile_image = serializers.ImageField(read_only=True)

    experience_years = serializers.IntegerField(read_only=True)
    experience_months = serializers.IntegerField(read_only=True)

    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
        source="categories_to_teach",
    )

    class Meta:
        model = InstructorProfile
        fields = [
            "id",
            "full_name",
            "email",
            "is_active",
            "profile_image",
            "occupation",
            "professional_bio",
            "education",
            "location",
            "experience_years",
            "experience_months",
            "categories",
            "linkedin_url",
            "github_url",
            "portfolio_url",
            "became_instructor_at",
            "created_at",
            "updated_at",
        ]


class InstructorStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=True)
