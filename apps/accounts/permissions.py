from rest_framework.permissions import BasePermission

from apps.instructors.models import InstructorProfile


class HasRole(BasePermission):
    allowed_roles = ()

    def has_permission(self, request, view):
        user = request.user

        return (
            user.is_authenticated and user.is_active and user.role in self.allowed_roles
        )


class IsStudent(HasRole):
    allowed_roles = ("student",)


class IsInstructor(HasRole):
    allowed_roles = ("instructor",)

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        try:
            return request.user.instructor_profile.is_active
        except InstructorProfile.DoesNotExist:
            return False


class IsStudentOrInstructor(HasRole):
    allowed_roles = ("student", "instructor")


class IsAdmin(HasRole):
    allowed_roles = ("admin",)
