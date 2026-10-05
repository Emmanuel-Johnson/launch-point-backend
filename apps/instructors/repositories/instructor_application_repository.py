from apps.accounts.models import User


class InstructorApplicationRepository:
    """Repository for instructor application database operations."""

    @staticmethod
    def get_application_form_data(user):
        return User.objects.select_related("student_profile").filter(id=user.id).first()
