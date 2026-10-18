from django.db.models import QuerySet

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
    def update_level_by_id(
        level_id: int,
        name: str,
        description: str = "",
    ) -> CourseLevel:
        return CourseLevelRepository.update_level_by_id(
            level_id=level_id,
            name=name,
            description=description,
        )

    @staticmethod
    def toggle_level_status_by_id(
        level_id: int,
    ) -> CourseLevel:
        return CourseLevelRepository.toggle_level_status_by_id(
            level_id=level_id,
        )
