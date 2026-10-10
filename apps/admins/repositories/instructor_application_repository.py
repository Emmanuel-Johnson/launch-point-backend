from django.utils import timezone

from apps.instructors.models import InstructorApplication


class InstructorApplicationRepository:
    @staticmethod
    def get_all_applications():
        return (
            InstructorApplication.objects.select_related("user")
            .prefetch_related("categories_to_teach")
            .order_by("-submitted_at")
        )

    @staticmethod
    def get_application_by_id(application_id):
        return (
            InstructorApplication.objects.select_related(
                "user",
                "reviewed_by",
            )
            .prefetch_related(
                "categories_to_teach",
                "supporting_documents",
            )
            .filter(id=application_id)
            .first()
        )

    @staticmethod
    def reject_application(application, admin, admin_message):
        application.status = InstructorApplication.Status.REJECTED
        application.admin_message = admin_message
        application.reviewed_at = timezone.now()
        application.reviewed_by = admin

        application.save(
            update_fields=[
                "status",
                "admin_message",
                "reviewed_at",
                "reviewed_by",
                "updated_at",
            ]
        )

        return application

    @staticmethod
    def get_application_for_rejection(application_id):
        return InstructorApplication.objects.filter(id=application_id).first()
