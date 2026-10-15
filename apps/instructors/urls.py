from django.urls import path

from apps.instructors.views.instructor_application_view import (
    InstructorApplicationDetailView,
    InstructorApplicationFormView,
    InstructorApplicationListView,
    InstructorDashboardOpenedView,
)
from apps.instructors.views.instructor_profile_view import (
    InstructorProfileView,
)
from apps.instructors.views.instructor_switch_view import SwitchToStudentView

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
    path(
        "applications/<int:application_id>/",
        InstructorApplicationDetailView.as_view(),
    ),
    path(
        "dashboard/opened/",
        InstructorDashboardOpenedView.as_view(),
        name="instructor-dashboard-opened",
    ),
    path("profile/", InstructorProfileView.as_view(), name="instructor-profile"),
    path(
        "switch-to-student/",
        SwitchToStudentView.as_view(),
        name="switch-to-student",
    ),
]
