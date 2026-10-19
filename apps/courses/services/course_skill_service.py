from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.courses.models import Skill
from apps.courses.repositories.course_skill_repository import (
    CourseSkillRepository,
)


class CourseSkillService:
    @staticmethod
    def create_skill(
        name: str,
        description: str = "",
    ) -> Skill:
        return CourseSkillRepository.create_skill(
            name=name,
            description=description,
        )

    @staticmethod
    def get_all_skills() -> QuerySet[Skill]:
        return CourseSkillRepository.get_all_skills()

    @staticmethod
    def get_skill_by_id(skill_id: int) -> Skill:
        return get_object_or_404(Skill, id=skill_id)

    @staticmethod
    def update_skill_by_id(
        skill: Skill,
        **validated_data,
    ) -> Skill:
        return CourseSkillRepository.update_skill_by_id(
            skill=skill,
            **validated_data,
        )

    @staticmethod
    def update_skill_status_by_id(
        skill: Skill,
        is_active: bool,
    ) -> Skill:
        return CourseSkillRepository.update_skill_status_by_id(
            skill=skill,
            is_active=is_active,
        )
