from apps.admins.repositories.instructor_application_repository import (
    InstructorApplicationRepository,
)


class InstructorApplicationService:
    @staticmethod
    def get_all_applications():
        return InstructorApplicationRepository.get_all_applications()
