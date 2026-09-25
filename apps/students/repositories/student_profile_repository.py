from apps.students.models import StudentProfile


class StudentProfileRepository:
    """Repository for student profile database operations."""

    DEFAULT_PROFILE_IMAGE = "profile_images/default_profile.png"

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

        old_image = profile.profile_image

        new_image = profile_data.get("profile_image")

        for field, value in profile_data.items():
            setattr(profile, field, value)

        if profile_data:
            profile.save()

        if user_data:
            for field, value in user_data.items():
                setattr(profile.user, field, value)

            profile.user.save()

        if (
            new_image == StudentProfileRepository.DEFAULT_PROFILE_IMAGE
            and old_image
            and old_image.name != StudentProfileRepository.DEFAULT_PROFILE_IMAGE
        ):
            old_image.delete(save=False)

        return profile
