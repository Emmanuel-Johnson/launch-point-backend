from django.urls import path

from apps.courses.views.admin.course_level_views import (
    CourseLevelDeleteView,
    CourseLevelListCreateView,
    CourseLevelStatusView,
    CourseLevelUpdateView,
)
from apps.courses.views.admin.skill_views import (
    SkillDeleteView,
    SkillListCreateView,
    SkillStatusView,
    SkillUpdateView,
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
    path(
        "levels/<int:pk>/delete/",
        CourseLevelDeleteView.as_view(),
        name="course-level-delete",
    ),
    path(
        "skills/",
        SkillListCreateView.as_view(),
        name="skill-list-create",
    ),
    path(
        "skills/<int:pk>/",
        SkillUpdateView.as_view(),
        name="skill-update",
    ),
    path(
        "skills/<int:pk>/status/",
        SkillStatusView.as_view(),
        name="skill-status",
    ),
    path(
        "skills/<int:pk>/delete/",
        SkillDeleteView.as_view(),
        name="skill-delete",
    ),
]
