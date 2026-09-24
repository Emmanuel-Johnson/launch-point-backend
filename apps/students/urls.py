from django.urls import path

from apps.students.views.student_profile_view import StudentProfileView

urlpatterns = [
    path(
        "student/profile/",
        StudentProfileView.as_view(),
        name="student-profile",
    ),
]
