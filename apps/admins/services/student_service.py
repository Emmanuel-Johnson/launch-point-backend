from rest_framework.exceptions import NotFound

from apps.admins.repositories.student_repository import StudentRepository


class StudentService:
    @staticmethod
    def get_students():
        return StudentRepository.get_all_students()

    @staticmethod
    def get_student(student_id):
        student = StudentRepository.get_student_by_id(student_id)

        if student is None:
            raise NotFound("Student not found.")

        return student
