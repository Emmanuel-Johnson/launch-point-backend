from rest_framework import serializers

from apps.categories.models import Category
from apps.instructors.models import InstructorProfile


class InstructorProfileSerializer(serializers.ModelSerializer):
    """Serializer for displaying an instructor profile."""

    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

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
        fields = (
            "id",
            "full_name",
            "email",
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
        )


class InstructorProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for validating instructor profile updates."""

    profile_image = serializers.ImageField(
        required=False,
        allow_null=True,
    )

    remove_profile_image = serializers.BooleanField(
        write_only=True,
        required=False,
        default=False,
    )

    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=False,
        source="categories_to_teach",
    )

    years_of_experience = serializers.ChoiceField(
        choices=InstructorProfile._meta.get_field("years_of_experience").choices,
        required=False,
    )

    class Meta:
        model = InstructorProfile
        fields = (
            "full_name",
            "profile_image",
            "remove_profile_image",
            "occupation",
            "professional_bio",
            "education",
            "location",
            "years_of_experience",
            "categories",
            "linkedin_url",
            "github_url",
            "portfolio_url",
        )

    def validate(self, attrs):
        if (
            attrs.get("remove_profile_image", False)
            and attrs.get("profile_image") is not None
        ):
            raise serializers.ValidationError(
                {
                    "profile_image": (
                        "Upload a new image or remove the existing image, not both."
                    )
                }
            )

        return attrs

    def validate_full_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Full name cannot be empty.")

        return value

    def validate_occupation(self, value):
        return value.strip()

    def validate_professional_bio(self, value):
        return value.strip()

    def validate_education(self, value):
        return value.strip()

    def validate_location(self, value):
        return value.strip()

    def validate_linkedin_url(self, value):
        return value.strip()

    def validate_github_url(self, value):
        return value.strip()

    def validate_portfolio_url(self, value):
        return value.strip()

    def validate_profile_image(self, value):
        if value is None:
            return value

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Only JPG, PNG, and WebP images are allowed."
            )

        max_size = 5 * 1024 * 1024

        if value.size > max_size:
            raise serializers.ValidationError("Profile image cannot exceed 5 MB.")

        return value
