from apps.accounts.models import User
from apps.instructors.models import (
    InstructorApplication,
    InstructorApplicationDocument,
)


class InstructorApplicationRepository:
    """Repository for instructor application database operations."""

    @staticmethod
    def get_application_form_data(user):
        return User.objects.select_related("student_profile").filter(id=user.id).first()

    @staticmethod
    def get_pending_application(user):
        return InstructorApplication.objects.filter(
            user=user,
            status=InstructorApplication.Status.PENDING,
        ).first()

    @staticmethod
    def create_application(user, **data):
        return InstructorApplication.objects.create(
            user=user,
            **data,
        )

    @staticmethod
    def set_application_categories(application, categories):
        application.categories_to_teach.set(categories)

    @staticmethod
    def create_supporting_document(application, document):
        return InstructorApplicationDocument.objects.create(
            application=application,
            document=document,
        )

    @staticmethod
    def get_user_applications(user):
        return (
            InstructorApplication.objects.filter(user=user)
            .prefetch_related("categories_to_teach")
            .order_by("-submitted_at")
        )
