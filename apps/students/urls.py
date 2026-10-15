from django.urls import path

from apps.students.views.student_profile_view import StudentProfileView
from apps.students.views.student_switch_view import SwitchToInstructorView

urlpatterns = [
    path(
        "profile/",
        StudentProfileView.as_view(),
        name="student-profile",
    ),
    path(
        "switch-to-instructor/",
        SwitchToInstructorView.as_view(),
        name="switch-to-instructor",
    ),
]
