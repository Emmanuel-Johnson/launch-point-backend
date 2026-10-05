from django.db import transaction

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
        """Update student profile and related user data."""

        old_image = profile.user.profile_image
        old_image_name = old_image.name if old_image else None
        old_image_storage = old_image.storage if old_image else None

        # Update profile fields.
        for field, value in profile_data.items():
            setattr(profile, field, value)

        if profile_data:
            profile.save()

        # Update related user fields.
        if user_data:
            for field, value in user_data.items():
                setattr(profile.user, field, value)

            profile.user.save()

        # Get the current image after saving.
        new_image = profile.user.profile_image
        new_image_name = new_image.name if new_image else None

        # Delete the previous uploaded image only if it was replaced.
        if (
            old_image_name
            and old_image_storage
            and old_image_name != StudentProfileRepository.DEFAULT_PROFILE_IMAGE
            and old_image_name != new_image_name
        ):
            transaction.on_commit(lambda: old_image_storage.delete(old_image_name))

        return profile
