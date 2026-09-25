from django.db import transaction

from apps.students.repositories.student_profile_repository import (
    StudentProfileRepository,
)


class StudentProfileService:
    """Service layer for student profile operations."""

    DEFAULT_PROFILE_IMAGE = "profile_images/default_profile.png"

    @staticmethod
    def get_profile(user):
        profile = StudentProfileRepository.get_by_user(user)

        if not profile:
            profile = StudentProfileRepository.create(user)

        return profile

    @staticmethod
    @transaction.atomic
    def update_profile(user, data):
        data = data.copy()

        profile = StudentProfileRepository.get_by_user(user)

        if not profile:
            profile = StudentProfileRepository.create(user)

        user_data = data.pop("user", {})

        remove_profile_image = data.pop(
            "remove_profile_image",
            False,
        )

        if remove_profile_image:
            data["profile_image"] = StudentProfileService.DEFAULT_PROFILE_IMAGE

        return StudentProfileRepository.update(
            profile=profile,
            profile_data=data,
            user_data=user_data,
        )
