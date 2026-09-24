from apps.students.models import StudentProfile


class StudentProfileRepository:
    """Repository for student profile database operations."""

    @staticmethod
    def get_by_user(user):
        return StudentProfile.objects.select_related("user").filter(user=user).first()

    @staticmethod
    def create(user):
        return StudentProfile.objects.create(user=user)

    @staticmethod
    def update(profile, data):
        for field, value in data.items():
            setattr(profile, field, value)

        profile.save()

        return profile
