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
    def update(profile, profile_data, user_data=None):
        """
        Update student profile and related user data.
        """

        for field, value in profile_data.items():
            setattr(profile, field, value)

        if profile_data:
            profile.save()

        if user_data:
            for field, value in user_data.items():
                setattr(profile.user, field, value)

            profile.user.save()

        return profile
