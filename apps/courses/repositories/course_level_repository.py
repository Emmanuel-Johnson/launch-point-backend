from typing import Any

from django.db.models import QuerySet

from apps.courses.models import CourseLevel


class CourseLevelRepository:
    @staticmethod
    def get_level_by_id(level_id: int) -> CourseLevel:
        return CourseLevel.objects.get(id=level_id)

    @staticmethod
    def get_all_levels() -> QuerySet[CourseLevel]:
        return CourseLevel.objects.all()

    @staticmethod
    def create_level(
        name: str,
        description: str = "",
        is_active: bool = True,
    ) -> CourseLevel:
        return CourseLevel.objects.create(
            name=name,
            description=description,
            is_active=is_active,
        )

    @staticmethod
    def update_level(
        level: CourseLevel,
        **validated_data: Any,
    ) -> CourseLevel:
        for field, value in validated_data.items():
            setattr(level, field, value)

        level.save()
        return level

    @staticmethod
    def update_level_status(
        level: CourseLevel,
        is_active: bool,
    ) -> CourseLevel:
        level.is_active = is_active
        level.save(update_fields=["is_active", "updated_at"])
        return level
