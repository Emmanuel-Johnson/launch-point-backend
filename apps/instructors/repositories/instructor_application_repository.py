from apps.accounts.models import User
from apps.categories.models import Category


class InstructorApplicationRepository:
    """Repository for instructor application database operations."""

    @staticmethod
    def get_application_form_data(user):
        return User.objects.select_related("student_profile").filter(id=user.id).first()

    @staticmethod
    def get_active_categories():
        return Category.objects.filter(is_active=True).values(
            "id",
            "name",
        )
