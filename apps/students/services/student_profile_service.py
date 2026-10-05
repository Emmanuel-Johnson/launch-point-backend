import logging

from django.db import transaction

from apps.students.repositories.student_profile_repository import (
    StudentProfileRepository,
)

logger = logging.getLogger(__name__)


class StudentProfileService:
    """Service layer for student profile operations."""

    DEFAULT_PROFILE_IMAGE = "profile_images/default_profile.png"

    @staticmethod
    def get_profile(user):
        logger.info(
            "Fetching student profile.",
            extra={"user_id": user.id},
        )

        profile = StudentProfileRepository.get_by_user(user)

        if not profile:
            logger.info(
                "No profile found; creating new profile.",
                extra={"user_id": user.id},
            )
            profile = StudentProfileRepository.create(user)

        logger.info(
            "Student profile fetched successfully.",
            extra={"user_id": user.id},
        )

        return profile

    @staticmethod
    @transaction.atomic
    def update_profile(user, data):
        logger.info(
            "Updating student profile.",
            extra={"user_id": user.id},
        )

        data = data.copy()

        profile = StudentProfileRepository.get_by_user(user)

        if not profile:
            logger.info(
                "No profile found; creating new profile before update.",
                extra={"user_id": user.id},
            )
            profile = StudentProfileRepository.create(user)

        user_data = data.pop("user", {})

        remove_profile_image = data.pop(
            "remove_profile_image",
            False,
        )

        if remove_profile_image:
            logger.info(
                "Removing profile image; resetting to default.",
                extra={"user_id": user.id},
            )
            user_data["profile_image"] = StudentProfileService.DEFAULT_PROFILE_IMAGE

        updated_profile = StudentProfileRepository.update(
            profile=profile,
            profile_data=data,
            user_data=user_data,
        )

        logger.info(
            "Student profile updated successfully.",
            extra={"user_id": user.id},
        )

        return updated_profile
