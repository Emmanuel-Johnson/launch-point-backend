from apps.instructors.models import InstructorProfile


class InstructorProfileRepository:
    @staticmethod
    def get_profile(user):
        return (
            InstructorProfile.objects.filter(user=user)
            .prefetch_related("categories_to_teach")
            .first()
        )
