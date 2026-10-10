from rest_framework.exceptions import NotFound, ValidationError

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

    @staticmethod
    def reject_application(application_id, admin, admin_message):
        application = InstructorApplicationRepository.get_application_for_rejection(
            application_id
        )

        if application is None:
            raise NotFound("Instructor application not found.")

        if application.status != "pending":
            raise ValidationError("Only pending applications can be rejected.")

        return InstructorApplicationRepository.reject_application(
            application=application,
            admin=admin,
            admin_message=admin_message,
        )
