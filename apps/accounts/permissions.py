from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Allow access only to authenticated users who are both staff and superuser.

    Request-level permission (has_permission); it performs no object-level
    checks.
    """

    message = "Admin access required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
            and request.user.is_superuser
        )
