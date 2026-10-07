import re
from urllib.parse import urlparse

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import URLValidator
from rest_framework import serializers

from apps.categories.models import Category
from apps.instructors.models import InstructorApplication

MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_PROFILE_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

ALLOWED_RESUME_TYPES = {
    "application/pdf",
}


def validate_file_size(file, field_name):
    if file and file.size > MAX_FILE_SIZE:
        raise serializers.ValidationError(f"{field_name} must be 5 MB or smaller.")


def validate_https_url(value, field_name):
    try:
        URLValidator()(value)
    except DjangoValidationError:
        raise serializers.ValidationError(f"Enter a valid {field_name} URL.")

    parsed_url = urlparse(value)

    if parsed_url.scheme != "https":
        raise serializers.ValidationError(f"{field_name} URL must use HTTPS.")

    return value


def validate_platform_url(value, allowed_domains, field_name):
    value = validate_https_url(
        value=value,
        field_name=field_name,
    )

    hostname = (urlparse(value).hostname or "").lower()

    if hostname not in allowed_domains:
        raise serializers.ValidationError(f"Enter a valid {field_name} URL.")

    return value


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
            "professional_bio",
            "phone_number",
            "location",
            "linkedin_url",
            "github_url",
            "portfolio_url",
            "motivation",
            "resume",
            "terms_accepted",
        )

        extra_kwargs = {
            "full_name": {
                "required": True,
                "allow_blank": False,
            },
            "occupation": {
                "required": True,
                "allow_blank": False,
            },
            "education": {
                "required": True,
                "allow_blank": False,
            },
            "years_of_experience": {
                "required": True,
                "allow_blank": False,
            },
            "professional_bio": {
                "required": True,
                "allow_blank": False,
            },
            "phone_number": {
                "required": True,
                "allow_blank": False,
            },
            "location": {
                "required": True,
                "allow_blank": False,
            },
            "linkedin_url": {
                "required": True,
                "allow_blank": False,
            },
            "github_url": {
                "required": True,
                "allow_blank": False,
            },
            "portfolio_url": {
                "required": True,
                "allow_blank": False,
            },
            "motivation": {
                "required": True,
                "allow_blank": False,
            },
            "resume": {
                "required": True,
            },
            "terms_accepted": {
                "required": True,
            },
        }

    # ---------------------------------------------------------
    # Full name
    # ---------------------------------------------------------

    def validate_full_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Full name is required.")

        if len(value) > 50:
            raise serializers.ValidationError("Full name cannot exceed 50 characters.")

        return value

    # ---------------------------------------------------------
    # Profile image
    # ---------------------------------------------------------

    def validate_profile_image(self, value):
        # Profile image is optional on the backend.
        # If provided, validate its size and actual uploaded type.
        if not value:
            return value

        validate_file_size(
            value,
            "Profile image",
        )

        if value.content_type not in ALLOWED_PROFILE_IMAGE_TYPES:
            raise serializers.ValidationError(
                "Please choose a valid JPG, PNG, or WebP image."
            )

        return value

    # ---------------------------------------------------------
    # Occupation
    # ---------------------------------------------------------

    def validate_occupation(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Occupation is required.")

        if len(value) > 100:
            raise serializers.ValidationError(
                "Occupation cannot exceed 100 characters."
            )

        return value

    # ---------------------------------------------------------
    # Education
    # ---------------------------------------------------------

    def validate_education(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Education is required.")

        if len(value) > 150:
            raise serializers.ValidationError("Education cannot exceed 150 characters.")

        return value

    # ---------------------------------------------------------
    # Experience
    # ---------------------------------------------------------

    def validate_years_of_experience(self, value):
        valid_values = {
            choice[0] for choice in InstructorApplication.Experience.choices
        }

        if value not in valid_values:
            raise serializers.ValidationError("Please select a valid experience level.")

        return value

    # ---------------------------------------------------------
    # Categories
    # ---------------------------------------------------------

    def validate_categories_to_teach(self, categories):
        if not categories:
            raise serializers.ValidationError("Select at least one category.")

        if len(categories) > 10:
            raise serializers.ValidationError("You can select up to 10 categories.")

        return categories

    # ---------------------------------------------------------
    # Professional bio
    # ---------------------------------------------------------

    def validate_professional_bio(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Professional bio is required.")

        if len(value) > 1000:
            raise serializers.ValidationError(
                "Professional bio cannot exceed 1000 characters."
            )

        return value

    # ---------------------------------------------------------
    # Phone number
    # ---------------------------------------------------------

    def validate_phone_number(self, value):
        value = value.strip()

        if not re.fullmatch(r"\d{10}", value):
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return value

    # ---------------------------------------------------------
    # Location
    # ---------------------------------------------------------

    def validate_location(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Location is required.")

        if len(value) > 100:
            raise serializers.ValidationError("Location cannot exceed 100 characters.")

        return value

    # ---------------------------------------------------------
    # LinkedIn
    # ---------------------------------------------------------

    def validate_linkedin_url(self, value):
        return validate_platform_url(
            value=value.strip(),
            allowed_domains={
                "linkedin.com",
                "www.linkedin.com",
            },
            field_name="LinkedIn",
        )

    # ---------------------------------------------------------
    # GitHub
    # ---------------------------------------------------------

    def validate_github_url(self, value):
        return validate_platform_url(
            value=value.strip(),
            allowed_domains={
                "github.com",
                "www.github.com",
            },
            field_name="GitHub",
        )

    # ---------------------------------------------------------
    # Portfolio
    # ---------------------------------------------------------

    def validate_portfolio_url(self, value):
        return validate_https_url(
            value=value.strip(),
            field_name="portfolio",
        )

    # ---------------------------------------------------------
    # Motivation
    # ---------------------------------------------------------

    def validate_motivation(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Motivation is required.")

        if len(value) > 1000:
            raise serializers.ValidationError(
                "Motivation cannot exceed 1000 characters."
            )

        return value

    # ---------------------------------------------------------
    # Resume
    # ---------------------------------------------------------

    def validate_resume(self, value):
        if not value:
            raise serializers.ValidationError("Please upload your resume.")

        validate_file_size(
            value,
            "Resume",
        )

        if value.content_type not in ALLOWED_RESUME_TYPES:
            raise serializers.ValidationError("Resume must be a PDF file.")

        return value

    # ---------------------------------------------------------
    # Terms
    # ---------------------------------------------------------

    def validate_terms_accepted(self, value):
        if value is not True:
            raise serializers.ValidationError(
                "You must accept the terms before submitting."
            )

        return value


class InstructorApplicationListSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = InstructorApplication
        fields = (
            "id",
            "categories",
            "submitted_at",
            "status",
        )

    def get_categories(self, obj):
        return list(obj.categories_to_teach.values_list("name", flat=True))
