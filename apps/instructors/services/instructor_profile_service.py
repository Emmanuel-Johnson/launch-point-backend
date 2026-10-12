from django.db import transaction
from rest_framework.exceptions import NotFound

from apps.instructors.repositories.instructor_profile_repository import (
    InstructorProfileRepository,
)


class InstructorProfileService:
    """Service layer for instructor profile operations."""

    @staticmethod
    def get_profile(user):
        profile = InstructorProfileRepository.get_profile(user=user)

        if profile is None:
            raise NotFound("Instructor profile not found.")

        return profile

    @staticmethod
    @transaction.atomic
    def update_profile(user, data):
        profile = InstructorProfileRepository.get_profile(user=user)

        if profile is None:
            raise NotFound("Instructor profile not found.")

        return InstructorProfileRepository.update(
            profile=profile,
            profile_data=data,
        )
