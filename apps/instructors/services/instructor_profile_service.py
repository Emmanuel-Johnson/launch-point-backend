from rest_framework.exceptions import NotFound

from apps.instructors.repositories.instructor_profile_repository import (
    InstructorProfileRepository,
)


class InstructorProfileService:
    @staticmethod
    def get_profile(user):
        profile = InstructorProfileRepository.get_profile(user=user)

        if profile is None:
            raise NotFound("Instructor profile not found.")

        return profile
