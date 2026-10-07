from django.urls import path

from apps.instructors.views.instructor_application_view import (
    InstructorApplicationFormView,
    InstructorApplicationListView,
)

urlpatterns = [
    path(
        "application/",
        InstructorApplicationFormView.as_view(),
        name="instructor-application-form",
    ),
    path(
        "applications/",
        InstructorApplicationListView.as_view(),
        name="instructor-application-list",
    ),
]
