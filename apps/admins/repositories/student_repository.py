from django.contrib.auth import get_user_model
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

User = get_user_model()


class StudentRepository:
    @staticmethod
    def get_all_students():
        return (
            User.objects.select_related("student_profile")
            .filter(
                role=User.Role.STUDENT,
                email_verified=True,
            )
            .order_by("-date_joined")
        )

    @staticmethod
    def get_student_by_id(student_id):
        return (
            User.objects.select_related("student_profile")
            .filter(
                id=student_id,
                role=User.Role.STUDENT,
                email_verified=True,
            )
            .first()
        )

    @staticmethod
    def update_status(student, is_active):
        student.is_active = is_active
        student.save(update_fields=["is_active", "updated_at"])

    @staticmethod
    def blacklist_all_refresh_tokens(student):
        outstanding_tokens = OutstandingToken.objects.filter(user=student)

        for outstanding_token in outstanding_tokens:
            BlacklistedToken.objects.get_or_create(token=outstanding_token)
