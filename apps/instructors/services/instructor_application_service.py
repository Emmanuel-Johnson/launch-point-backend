from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.categories.repositories import CategoryRepository
from apps.instructors.repositories.instructor_application_repository import (
    InstructorApplicationRepository,
)


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
    @transaction.atomic
    def submit_application(user, validated_data, supporting_files):
        existing_application = InstructorApplicationRepository.get_pending_application(
            user=user,
        )

        if existing_application:
            raise ValidationError("You already have a pending instructor application.")

        categories = validated_data.pop("categories_to_teach")

        application = InstructorApplicationRepository.create_application(
            user=user,
            **validated_data,
        )

        InstructorApplicationRepository.set_application_categories(
            application=application,
            categories=categories,
        )

        for document in supporting_files:
            InstructorApplicationRepository.create_supporting_document(
                application=application,
                document=document,
            )

        return application
