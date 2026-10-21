from django.db import models
from django.db.models import Value
from django.db.models.functions import Length, Lower
from django.db.models.lookups import GreaterThanOrEqual


class CourseLevel(models.Model):
    name = models.CharField(
        max_length=50,
    )
    description = models.CharField(
        max_length=300,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "course_levels"
        ordering = ["-created_at"]
        verbose_name = "Course Level"
        verbose_name_plural = "Course Levels"
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                condition=models.Q(is_deleted=False),
                name="unique_course_level_name",
            ),
            models.CheckConstraint(
                condition=GreaterThanOrEqual(
                    Length("name"),
                    Value(3),
                ),
                name="course_level_name_min_length",
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Skill(models.Model):
    name = models.CharField(
        max_length=50,
    )
    description = models.CharField(
        max_length=300,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "skills"
        ordering = ["-created_at"]
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                condition=models.Q(is_deleted=False),
                name="unique_skill_name",
            ),
            models.CheckConstraint(
                condition=GreaterThanOrEqual(
                    Length("name"),
                    Value(3),
                ),
                name="skill_name_min_length",
            ),
        ]

    def __str__(self) -> str:
        return self.name
