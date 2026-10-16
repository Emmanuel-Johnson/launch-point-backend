from rest_framework.exceptions import PermissionDenied
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
        user = request.user

        if not user.is_authenticated or not user.is_active:
            return False

        if user.role != "instructor":
            raise PermissionDenied(
                detail={
                    "code": "instructor_access_denied",
                    "message": "You do not have instructor access.",
                }
            )

        try:
            instructor_profile = user.instructor_profile
        except InstructorProfile.DoesNotExist:
            raise PermissionDenied(
                detail={
                    "code": "instructor_access_denied",
                    "message": "You do not have instructor access.",
                }
            )

        if not instructor_profile.is_active:
            raise PermissionDenied(
                detail={
                    "code": "instructor_access_denied",
                    "message": "You do not have instructor access.",
                }
            )

        return True


class IsStudentOrInstructor(HasRole):
    allowed_roles = ("student", "instructor")


class IsAdmin(HasRole):
    allowed_roles = ("admin",)
