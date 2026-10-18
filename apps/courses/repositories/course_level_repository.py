from django.db import models

from apps.courses.models import CourseLevel


class CourseLevelRepository:
    @staticmethod
    def create_level(
        name: str,
        description: str = "",
    ) -> CourseLevel:
        return CourseLevel.objects.create(
            name=name,
            description=description,
        )

    @staticmethod
    def get_all_levels() -> models.QuerySet[CourseLevel]:
        return CourseLevel.objects.all()

    @staticmethod
    def update_level_by_id(
        level_id: int,
        name: str,
        description: str = "",
    ) -> CourseLevel:
        level = CourseLevel.objects.get(id=level_id)

        level.name = name
        level.description = description
        level.save(update_fields=["name", "description", "updated_at"])

        return level

    @staticmethod
    def toggle_level_status_by_id(level_id: int) -> CourseLevel:
        level = CourseLevel.objects.get(id=level_id)

        level.is_active = not level.is_active
        level.save(update_fields=["is_active", "updated_at"])

        return level
