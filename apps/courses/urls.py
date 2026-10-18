from django.urls import path

from apps.courses.views.course_level_views import (
    CourseLevelListCreateView,
    CourseLevelToggleStatusView,
    CourseLevelUpdateView,
)

urlpatterns = [
    path(
        "levels/",
        CourseLevelListCreateView.as_view(),
        name="course-level-list-create",
    ),
    path(
        "levels/<int:level_id>/",
        CourseLevelUpdateView.as_view(),
        name="course-level-update",
    ),
    path(
        "levels/<int:level_id>/status/",
        CourseLevelToggleStatusView.as_view(),
        name="course-level-status",
    ),
]
