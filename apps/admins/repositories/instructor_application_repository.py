from apps.instructors.models import InstructorApplication


class InstructorApplicationRepository:
    @staticmethod
    def get_all_applications():
        return (
            InstructorApplication.objects.select_related("user")
            .prefetch_related("categories_to_teach")
            .order_by("-submitted_at")
        )
