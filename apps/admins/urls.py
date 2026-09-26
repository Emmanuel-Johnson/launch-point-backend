from django.urls import path

from apps.admins.views.student_view import (
    AdminStudentDetailView,
    AdminStudentListView,
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
]
