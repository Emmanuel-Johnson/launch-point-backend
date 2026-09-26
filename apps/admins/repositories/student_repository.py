from django.contrib.auth import get_user_model

User = get_user_model()


class StudentRepository:
    @staticmethod
    def get_all_students():
        return (
            User.objects.select_related("student_profile")
            .filter(role=User.Role.STUDENT)
            .order_by("-date_joined")
        )

    @staticmethod
    def get_student_by_id(student_id):
        return (
            User.objects.select_related("student_profile")
            .filter(
                id=student_id,
                role=User.Role.STUDENT,
            )
            .first()
        )
