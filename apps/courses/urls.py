from django.urls import path

from apps.courses.views.course_level_views import (
    CourseLevelListCreateView,
    CourseLevelStatusView,
    CourseLevelUpdateView,
)

urlpatterns = [
    path(
        "levels/",
        CourseLevelListCreateView.as_view(),
        name="course-level-list-create",
    ),
    path(
        "levels/<int:pk>/",
        CourseLevelUpdateView.as_view(),
        name="course-level-update",
    ),
    path(
        "levels/<int:pk>/status/",
        CourseLevelStatusView.as_view(),
        name="course-level-status",
    ),
]
