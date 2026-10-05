from django.urls import path

from apps.instructors.views.instructor_application_view import (
    InstructorApplicationFormView,
)

urlpatterns = [
    path(
        "application/",
        InstructorApplicationFormView.as_view(),
        name="instructor-application-form",
    ),
]
