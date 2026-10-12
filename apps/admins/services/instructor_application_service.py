from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError

from apps.accounts.models import User
from apps.admins.repositories.instructor_application_repository import (
    InstructorApplicationRepository,
)
from apps.instructors.models import InstructorApplication


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

    @staticmethod
    @transaction.atomic
    def approve_application(application_id, admin, admin_message):
        application = InstructorApplicationRepository.get_application_for_approval(
            application_id
        )

        if application is None:
            raise NotFound("Instructor application not found.")

        if application.status != InstructorApplication.Status.PENDING:
            raise ValidationError("Only pending applications can be approved.")

        application = InstructorApplicationRepository.approve_application(
            application=application,
            admin=admin,
            admin_message=admin_message,
        )

        InstructorApplicationRepository.create_instructor_profile_from_application(
            application=application,
        )

        user = application.user

        if user.role != User.Role.INSTRUCTOR:
            InstructorApplicationRepository.update_user_role(
                user=user,
                role=User.Role.INSTRUCTOR,
            )

        return application
