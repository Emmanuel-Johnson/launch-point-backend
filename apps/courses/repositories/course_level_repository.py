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
        level: CourseLevel,
        **validated_data,
    ) -> CourseLevel:
        for field, value in validated_data.items():
            setattr(level, field, value)

        level.save()

        return level

    @staticmethod
    def update_level_status_by_id():
        pass
