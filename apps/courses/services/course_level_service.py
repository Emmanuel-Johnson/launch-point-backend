from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.courses.models import CourseLevel
from apps.courses.repositories.course_level_repository import (
    CourseLevelRepository,
)


class CourseLevelService:
    @staticmethod
    def create_level(
        name: str,
        description: str = "",
    ) -> CourseLevel:
        return CourseLevelRepository.create_level(
            name=name,
            description=description,
        )

    @staticmethod
    def get_all_levels() -> QuerySet[CourseLevel]:
        return CourseLevelRepository.get_all_levels()

    @staticmethod
    def get_level_by_id(level_id: int) -> CourseLevel:
        return get_object_or_404(CourseLevel, id=level_id)

    @staticmethod
    def update_level_by_id(
        level: CourseLevel,
        **validated_data,
    ) -> CourseLevel:
        return CourseLevelRepository.update_level_by_id(
            level=level,
            **validated_data,
        )

    @staticmethod
    def update_level_status_by_id(
        level: CourseLevel,
        is_active: bool,
    ) -> CourseLevel:
        return CourseLevelRepository.update_level_status_by_id(
            level=level,
            is_active=is_active,
        )
