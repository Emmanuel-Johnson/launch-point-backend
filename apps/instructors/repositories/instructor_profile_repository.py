from django.db import transaction

from apps.instructors.models import InstructorProfile


class InstructorProfileRepository:
    """Repository for instructor profile database operations."""

    @staticmethod
    def get_profile(user):
        return (
            InstructorProfile.objects.select_related("user")
            .prefetch_related("categories_to_teach")
            .filter(user=user)
            .first()
        )

    @staticmethod
    def update(profile, profile_data):
        """Update instructor profile fields and teaching categories."""

        profile_data = profile_data.copy()

        categories = profile_data.pop("categories_to_teach", None)
        remove_profile_image = profile_data.pop(
            "remove_profile_image",
            False,
        )

        # Keep a reference to the previous image for cleanup.
        old_image = profile.profile_image
        old_image_name = old_image.name if old_image else None
        old_image_storage = old_image.storage if old_image else None

        # Remove the existing image when explicitly requested.
        if remove_profile_image:
            profile.profile_image = None

        # Update regular profile fields.
        for field, value in profile_data.items():
            setattr(profile, field, value)

        profile.save()

        # Update categories only when supplied in the request.
        if categories is not None:
            profile.categories_to_teach.set(categories)

        # Delete the previous image only after the database transaction
        # commits successfully and only if it was replaced or removed.
        new_image = profile.profile_image
        new_image_name = new_image.name if new_image else None

        if old_image_name and old_image_storage and old_image_name != new_image_name:
            transaction.on_commit(lambda: old_image_storage.delete(old_image_name))

        return profile
