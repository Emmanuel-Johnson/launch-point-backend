from rest_framework import serializers

from apps.instructors.models import InstructorProfile


class InstructorListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    profile_image = serializers.ImageField(read_only=True)

    years_of_experience = serializers.CharField(
        source="get_years_of_experience_display",
        read_only=True,
    )

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
            "years_of_experience",
            "categories",
            "became_instructor_at",
        ]


class InstructorDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    profile_image = serializers.ImageField(read_only=True)

    years_of_experience = serializers.CharField(
        source="get_years_of_experience_display",
        read_only=True,
    )

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
            "years_of_experience",
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
