from django.db import transaction

from apps.students.repositories.student_profile_repository import (
    StudentProfileRepository,
)


class StudentProfileService:
    """Service layer for student profile operations."""

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

        return StudentProfileRepository.update(
            profile=profile,
            profile_data=data,
            user_data=user_data,
        )
