from apps.admins.repositories.instructor_application_repository import (
    InstructorApplicationRepository,
)


class InstructorApplicationService:
    @staticmethod
    def get_all_applications():
        return InstructorApplicationRepository.get_all_applications()

    @staticmethod
    def get_application_by_id(application_id):
        return InstructorApplicationRepository.get_application_by_id(application_id)
