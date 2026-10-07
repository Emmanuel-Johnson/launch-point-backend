from pathlib import Path

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.categories.repositories import CategoryRepository
from apps.instructors.repositories.instructor_application_repository import (
    InstructorApplicationRepository,
)

MAX_SUPPORTING_FILES = 10
MIN_SUPPORTING_FILES = 3
MAX_SUPPORTING_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_SUPPORTING_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
}


class InstructorApplicationService:
    """Service for instructor application operations."""

    @staticmethod
    def get_application_form_data(user):
        user_data = InstructorApplicationRepository.get_application_form_data(
            user=user,
        )

        categories = CategoryRepository.get_active_categories()

        return {
            "user": user_data,
            "categories": categories,
        }

    @staticmethod
    def validate_supporting_files(supporting_files):
        """
        Validate supporting documents before creating
        the instructor application.
        """

        file_count = len(supporting_files)

        # -----------------------------------------------------
        # File count
        # -----------------------------------------------------

        if file_count < MIN_SUPPORTING_FILES:
            raise ValidationError(
                {
                    "supporting_files": (
                        f"Please upload at least "
                        f"{MIN_SUPPORTING_FILES} supporting files."
                    )
                }
            )

        if file_count > MAX_SUPPORTING_FILES:
            raise ValidationError(
                {
                    "supporting_files": (
                        f"You can upload up to {MAX_SUPPORTING_FILES} supporting files."
                    )
                }
            )

        seen_files = set()

        for file in supporting_files:
            # -------------------------------------------------
            # File size
            # -------------------------------------------------

            if file.size > MAX_SUPPORTING_FILE_SIZE:
                raise ValidationError(
                    {"supporting_files": (f"{file.name} must be 5 MB or smaller.")}
                )

            # -------------------------------------------------
            # File type
            # -------------------------------------------------

            extension = Path(file.name).suffix.lower()

            if extension not in ALLOWED_SUPPORTING_EXTENSIONS:
                raise ValidationError(
                    {
                        "supporting_files": (
                            "Each supporting file must be PDF, PNG, JPG, or JPEG."
                        )
                    }
                )

            # -------------------------------------------------
            # Duplicate files
            # -------------------------------------------------

            file_signature = (
                file.name.lower(),
                file.size,
            )

            if file_signature in seen_files:
                raise ValidationError(
                    {
                        "supporting_files": (
                            "Duplicate supporting files are not allowed."
                        )
                    }
                )

            seen_files.add(file_signature)

    @staticmethod
    @transaction.atomic
    def submit_application(user, validated_data, supporting_files):
        # -----------------------------------------------------
        # Check existing pending application
        # -----------------------------------------------------

        existing_application = InstructorApplicationRepository.get_pending_application(
            user=user,
        )

        if existing_application:
            raise ValidationError(
                {"detail": ("You already have a pending instructor application.")}
            )

        # -----------------------------------------------------
        # Validate supporting files
        # -----------------------------------------------------

        InstructorApplicationService.validate_supporting_files(
            supporting_files=supporting_files,
        )

        # -----------------------------------------------------
        # Extract categories
        # -----------------------------------------------------

        categories = validated_data.pop(
            "categories_to_teach",
        )

        # -----------------------------------------------------
        # Create application
        # -----------------------------------------------------

        application = InstructorApplicationRepository.create_application(
            user=user,
            **validated_data,
        )

        # -----------------------------------------------------
        # Set categories
        # -----------------------------------------------------

        InstructorApplicationRepository.set_application_categories(
            application=application,
            categories=categories,
        )

        # -----------------------------------------------------
        # Create supporting documents
        # -----------------------------------------------------

        for document in supporting_files:
            InstructorApplicationRepository.create_supporting_document(
                application=application,
                document=document,
            )

        return application

    @staticmethod
    def get_user_applications(user):
        return InstructorApplicationRepository.get_user_applications(user=user)

    @staticmethod
    def get_user_application_detail(user, application_id):
        application = InstructorApplicationRepository.get_user_application_detail(
            user=user,
            application_id=application_id,
        )

        if not application:
            raise ValidationError({"detail": "Instructor application not found."})

        return application
