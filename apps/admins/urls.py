from django.urls import path

from apps.admins.views.instructor_application_view import (
    AdminInstructorApplicationListView,
)
from apps.admins.views.student_view import (
    AdminStudentDetailView,
    AdminStudentListView,
    AdminStudentStatusView,
)

urlpatterns = [
    path(
        "students/",
        AdminStudentListView.as_view(),
        name="admin-student-list",
    ),
    path(
        "students/<int:student_id>/",
        AdminStudentDetailView.as_view(),
        name="admin-student-detail",
    ),
    path(
        "students/<int:student_id>/status/",
        AdminStudentStatusView.as_view(),
        name="admin-student-status",
    ),
    path(
        "instructor-applications/",
        AdminInstructorApplicationListView.as_view(),
        name="admin-instructor-application-list",
    ),
]
