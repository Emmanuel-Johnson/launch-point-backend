from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    allowed_roles = ()

    def has_permission(self, request, view):
        user = request.user

        return (
            user.is_authenticated and user.is_active and user.role in self.allowed_roles
        )


class IsStudentOrInstructor(HasRole):
    allowed_roles = ("student", "instructor")


class IsInstructor(HasRole):
    allowed_roles = "instructor"


class IsAdmin(HasRole):
    allowed_roles = ("admin",)
