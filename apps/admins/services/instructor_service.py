import logging

from rest_framework.exceptions import NotFound

from apps.admins.repositories.instructor_repository import (
    InstructorRepository,
)

logger = logging.getLogger(__name__)


class InstructorService:
    @staticmethod
    def get_instructors():
        logger.info("Fetching all instructors.")

        instructors = InstructorRepository.get_all_instructors()

        logger.info("Fetched instructors successfully.")

        return instructors

    @staticmethod
    def get_instructor(instructor_id):
        logger.info(
            "Fetching instructor by ID.",
            extra={"instructor_id": instructor_id},
        )

        instructor = InstructorRepository.get_instructor_by_id(instructor_id)

        if instructor is None:
            logger.warning(
                "Instructor not found.",
                extra={"instructor_id": instructor_id},
            )
            raise NotFound("Instructor not found.")

        logger.info(
            "Fetched instructor successfully.",
            extra={"instructor_id": instructor_id},
        )

        return instructor
