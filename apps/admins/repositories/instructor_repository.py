from apps.instructors.models import InstructorProfile


class InstructorRepository:
    @staticmethod
    def get_all_instructors():
        return (
            InstructorProfile.objects.select_related("user")
            .prefetch_related("categories_to_teach")
            .order_by("-became_instructor_at")
        )

    @staticmethod
    def get_instructor_by_id(instructor_id):
        return (
            InstructorProfile.objects.select_related("user")
            .prefetch_related("categories_to_teach")
            .filter(id=instructor_id)
            .first()
        )

    @staticmethod
    def get_instructor_profile_by_id(instructor_id):
        return (
            InstructorProfile.objects.select_related("user")
            .filter(id=instructor_id)
            .first()
        )

    @staticmethod
    def update_instructor_status(instructor, is_active):
        instructor.is_active = is_active
        instructor.save(update_fields=["is_active", "updated_at"])

        instructor.user.role = "instructor" if is_active else "student"
        instructor.user.save(update_fields=["role"])

        return instructor
