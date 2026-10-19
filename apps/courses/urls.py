from django.urls import path

from apps.courses.views.course_level_views import (
    CourseLevelListCreateView,
    CourseLevelToggleStatusView,
    CourseLevelUpdateView,
)
from apps.courses.views.skill_views import (
    CourseSkillListCreateView,
    CourseSkillToggleStatusView,
    CourseSkillUpdateView,
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
    path(
        "skills/",
        CourseSkillListCreateView.as_view(),
        name="course-skill-list-create",
    ),
    path(
        "skills/<int:skill_id>/",
        CourseSkillUpdateView.as_view(),
        name="course-skill-update",
    ),
    path(
        "skills/<int:skill_id>/status/",
        CourseSkillToggleStatusView.as_view(),
        name="course-skill-status",
    ),
]
