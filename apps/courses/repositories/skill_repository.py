from django.db import models

from apps.courses.models import Skill


class CourseSkillRepository:
    @staticmethod
    def create_skill(
        name: str,
        description: str = "",
    ) -> Skill:
        return Skill.objects.create(
            name=name,
            description=description,
        )

    @staticmethod
    def get_all_skills() -> models.QuerySet[Skill]:
        return Skill.objects.all()

    @staticmethod
    def update_skill_by_id(
        skill: Skill,
        **validated_data,
    ) -> Skill:
        for field, value in validated_data.items():
            setattr(skill, field, value)

        skill.save()

        return skill

    @staticmethod
    def update_skill_status_by_id(
        skill: Skill,
        is_active: bool,
    ) -> Skill:
        skill.is_active = is_active

        skill.save(update_fields=["is_active", "updated_at"])

        return skill
