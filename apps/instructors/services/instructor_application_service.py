from apps.categories.repositories import CategoryRepository
from apps.instructors.repositories.instructor_application_repository import (
    InstructorApplicationRepository,
)


class InstructorApplicationService:
    """Service for instructor application operations."""

    @staticmethod
    def get_application_form_data(user):
        user_data = InstructorApplicationRepository.get_application_form_data(user=user)

        categories = CategoryRepository.get_active_categories()

        return {
            "user": user_data,
            "categories": categories,
        }
