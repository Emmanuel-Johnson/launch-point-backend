import logging

from django.db import transaction
from rest_framework.exceptions import NotFound

from apps.admins.repositories.student_repository import StudentRepository

logger = logging.getLogger(__name__)


class StudentService:
    @staticmethod
    def get_students():
        logger.info("Fetching all students.")

        students = StudentRepository.get_all_students()

        logger.info("Fetched all students successfully.")

        return students

    @staticmethod
    def get_student(student_id):
        logger.info(
            "Fetching student by id.",
            extra={"student_id": student_id},
        )

        student = StudentRepository.get_student_by_id(student_id)

        if student is None:
            logger.warning(
                "Student not found.",
                extra={"student_id": student_id},
            )
            raise NotFound("Student not found.")

        logger.info(
            "Fetched student successfully.",
            extra={"student_id": student_id},
        )

        return student

    @staticmethod
    @transaction.atomic
    def update_student_status(student_id, is_active):
        logger.info(
            "Updating student status.",
            extra={"student_id": student_id, "is_active": is_active},
        )

        student = StudentRepository.get_student_by_id(student_id)

        if student is None:
            logger.warning(
                "Student not found for status update.",
                extra={"student_id": student_id},
            )
            raise NotFound("Student not found.")

        StudentRepository.update_status(student, is_active)

        StudentRepository.blacklist_all_refresh_tokens(student)

        logger.info(
            "Student status updated and refresh tokens blacklisted.",
            extra={"student_id": student_id, "is_active": is_active},
        )

        return student
