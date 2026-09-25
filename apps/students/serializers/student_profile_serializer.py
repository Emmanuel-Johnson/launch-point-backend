from rest_framework import serializers

from apps.accounts.validators import validate_full_name
from apps.students.models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="user.full_name",
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    remove_profile_image = serializers.BooleanField(
        write_only=True,
        required=False,
        default=False,
    )

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "full_name",
            "email",
            "profile_image",
            "remove_profile_image",
            "bio",
            "location",
            "education",
            "occupation",
            "github_url",
            "linkedin_url",
            "portfolio_url",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "email",
            "created_at",
            "updated_at",
        ]

    def validate_full_name(self, value):
        return validate_full_name(value)

    def _has_repeated_special_character(self, value):
        for current, next_char in zip(value, value[1:]):
            if current == next_char and not current.isalnum() and not current.isspace():
                return True

        return False

    def validate_profile_image(self, value):
        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Only JPG, PNG, and WebP images are allowed."
            )

        max_size = 5 * 1024 * 1024  # 5 MB

        if value.size > max_size:
            raise serializers.ValidationError("Profile image cannot exceed 5 MB.")

        return value

    def validate_bio(self, value):
        value = value.strip()

        if not 10 <= len(value) <= 500:
            raise serializers.ValidationError(
                "Bio must be between 10 and 500 characters."
            )

        if self._has_repeated_special_character(value):
            raise serializers.ValidationError(
                "The same special character cannot be repeated consecutively."
            )

        return value

    def validate_location(self, value):
        value = value.strip()

        if not 3 <= len(value) <= 100:
            raise serializers.ValidationError(
                "Location must be between 3 and 100 characters."
            )

        if self._has_repeated_special_character(value):
            raise serializers.ValidationError(
                "The same special character cannot be repeated consecutively."
            )

        return value

    def validate_education(self, value):
        value = value.strip()

        if not 3 <= len(value) <= 150:
            raise serializers.ValidationError(
                "Education must be between 3 and 150 characters."
            )

        if self._has_repeated_special_character(value):
            raise serializers.ValidationError(
                "The same special character cannot be repeated consecutively."
            )

        return value

    def validate_occupation(self, value):
        value = value.strip()

        if not 3 <= len(value) <= 100:
            raise serializers.ValidationError(
                "Occupation must be between 3 and 100 characters."
            )

        if self._has_repeated_special_character(value):
            raise serializers.ValidationError(
                "The same special character cannot be repeated consecutively."
            )

        return value

    def validate_github_url(self, value):
        return value.strip()

    def validate_linkedin_url(self, value):
        return value.strip()

    def validate_portfolio_url(self, value):
        return value.strip()
