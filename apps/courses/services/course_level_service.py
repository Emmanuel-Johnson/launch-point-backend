from typing import Any

from django.db.models import QuerySet

from apps.courses.models import CourseLevel
from apps.courses.repositories.course_level_repository import (
    CourseLevelRepository,
)


class CourseLevelService:
    @staticmethod
    def get_level_by_id(level_id: int) -> CourseLevel:
        return CourseLevelRepository.get_level_by_id(level_id)

    @staticmethod
    def get_all_levels() -> QuerySet[CourseLevel]:
        return CourseLevelRepository.get_all_levels()

    @staticmethod
    def create_level(
        name: str,
        description: str = "",
        is_active: bool = True,
    ) -> CourseLevel:
        return CourseLevelRepository.create_level(
            name=name,
            description=description,
            is_active=is_active,
        )

    @staticmethod
    def update_level(
        level: CourseLevel,
        **validated_data: Any,
    ) -> CourseLevel:
        return CourseLevelRepository.update_level(
            level=level,
            **validated_data,
        )

    @staticmethod
    def update_level_status(
        level: CourseLevel,
        is_active: bool,
    ) -> CourseLevel:
        return CourseLevelRepository.update_level_status(
            level=level,
            is_active=is_active,
        )

    @staticmethod
    def soft_delete_level(level: CourseLevel) -> CourseLevel:
        return CourseLevelRepository.soft_delete_level(level=level)
