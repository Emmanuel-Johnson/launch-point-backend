from django.urls import path

from apps.admins.views.instructor_application_view import (
    AdminInstructorApplicationApproveView,
    AdminInstructorApplicationDetailView,
    AdminInstructorApplicationListView,
    AdminInstructorApplicationRejectView,
)
from apps.admins.views.instructor_view import (
    AdminInstructorDetailView,
    AdminInstructorListView,
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
    path(
        "instructor-applications/<int:application_id>/",
        AdminInstructorApplicationDetailView.as_view(),
        name="admin-instructor-application-detail",
    ),
    path(
        "instructor-applications/<int:application_id>/reject/",
        AdminInstructorApplicationRejectView.as_view(),
        name="admin-reject-instructor-application",
    ),
    path(
        "instructor-applications/<int:application_id>/approve/",
        AdminInstructorApplicationApproveView.as_view(),
        name="admin-approve-instructor-application",
    ),
    path(
        "instructors/",
        AdminInstructorListView.as_view(),
        name="admin-instructor-list",
    ),
    path(
        "instructors/<int:instructor_id>/",
        AdminInstructorDetailView.as_view(),
        name="admin-instructor-detail",
    ),
]
