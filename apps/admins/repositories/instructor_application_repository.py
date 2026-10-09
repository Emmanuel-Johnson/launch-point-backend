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
