from django.urls import path

from apps.instructors.views.instructor_application_view import (
    InstructorApplicationCreateView,
)

urlpatterns = [
    path(
        "applications/",
        InstructorApplicationCreateView.as_view(),
        name="instructor-application-create",
    ),
]
