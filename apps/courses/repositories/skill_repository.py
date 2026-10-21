from typing import Any

from django.db.models import QuerySet
from django.utils import timezone

from apps.courses.models import Skill


class SkillRepository:
    @staticmethod
    def get_skill_by_id(skill_id: int) -> Skill:
        return Skill.objects.get(id=skill_id, is_deleted=False)

    @staticmethod
    def get_all_skills() -> QuerySet[Skill]:
        return Skill.objects.filter(is_deleted=False)

    @staticmethod
    def create_skill(
        name: str,
        description: str = "",
        is_active: bool = True,
    ) -> Skill:
        return Skill.objects.create(
            name=name,
            description=description,
            is_active=is_active,
        )

    @staticmethod
    def update_skill(
        skill: Skill,
        **validated_data: Any,
    ) -> Skill:
        for field, value in validated_data.items():
            setattr(skill, field, value)

        skill.save()
        return skill

    @staticmethod
    def update_skill_status(
        skill: Skill,
        is_active: bool,
    ) -> Skill:
        skill.is_active = is_active
        skill.save(update_fields=["is_active", "updated_at"])
        return skill

    @staticmethod
    def soft_delete_skill(skill: Skill) -> Skill:
        skill.is_deleted = True
        skill.deleted_at = timezone.now()
        skill.save(update_fields=["is_deleted", "deleted_at"])
        return skill
