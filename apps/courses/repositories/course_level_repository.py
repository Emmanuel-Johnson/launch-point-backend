from typing import Any

from django.db.models import QuerySet
from django.utils import timezone

from apps.courses.models import CourseLevel


class CourseLevelRepository:
    @staticmethod
    def get_level_by_id(level_id: int) -> CourseLevel:
        return CourseLevel.objects.get(id=level_id, is_deleted=False)

    @staticmethod
    def get_all_levels() -> QuerySet[CourseLevel]:
        return CourseLevel.objects.filter(is_deleted=False)

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

    @staticmethod
    def soft_delete_level(level: CourseLevel) -> CourseLevel:
        level.is_deleted = True
        level.deleted_at = timezone.now()
        level.save(update_fields=["is_deleted", "deleted_at"])
        return level
