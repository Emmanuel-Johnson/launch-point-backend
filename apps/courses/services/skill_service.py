from typing import Any

from django.db.models import QuerySet

from apps.courses.models import Skill
from apps.courses.repositories.skill_repository import (
    SkillRepository,
)


class SkillService:
    @staticmethod
    def get_skill_by_id(skill_id: int) -> Skill:
        return SkillRepository.get_skill_by_id(skill_id)

    @staticmethod
    def get_all_skills() -> QuerySet[Skill]:
        return SkillRepository.get_all_skills()

    @staticmethod
    def create_skill(
        name: str,
        description: str = "",
        is_active: bool = True,
    ) -> Skill:
        return SkillRepository.create_skill(
            name=name,
            description=description,
            is_active=is_active,
        )

    @staticmethod
    def update_skill(
        skill: Skill,
        **validated_data: Any,
    ) -> Skill:
        return SkillRepository.update_skill(
            skill=skill,
            **validated_data,
        )

    @staticmethod
    def update_skill_status(
        skill: Skill,
        is_active: bool,
    ) -> Skill:
        return SkillRepository.update_skill_status(
            skill=skill,
            is_active=is_active,
        )

    @staticmethod
    def soft_delete_skill(skill: Skill) -> Skill:
        return SkillRepository.soft_delete_skill(skill=skill)
