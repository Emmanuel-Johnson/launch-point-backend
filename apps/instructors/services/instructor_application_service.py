from apps.instructors.repositories.instructor_application_repository import (
    InstructorApplicationRepository,
)


class InstructorApplicationService:
    """Service for instructor application operations."""

    @staticmethod
    def get_application_form_data(user):
        return InstructorApplicationRepository.get_application_form_data(user=user)
