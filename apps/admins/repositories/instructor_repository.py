from apps.instructors.models import InstructorProfile


class InstructorRepository:
    @staticmethod
    def get_all_instructors():
        return (
            InstructorProfile.objects.select_related("user")
            .prefetch_related("categories_to_teach")
            .filter(user__role="instructor")
            .order_by("-became_instructor_at")
        )

    @staticmethod
    def get_instructor_by_id(instructor_id):
        return (
            InstructorProfile.objects.select_related("user")
            .prefetch_related("categories_to_teach")
            .filter(
                id=instructor_id,
                user__role="instructor",
            )
            .first()
        )
