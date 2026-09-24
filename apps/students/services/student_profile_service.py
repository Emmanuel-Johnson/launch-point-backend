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
    def update_profile(user, data):
        profile = StudentProfileRepository.get_by_user(user)

        if not profile:
            profile = StudentProfileRepository.create(user)

        return StudentProfileRepository.update(
            profile=profile,
            data=data,
        )
