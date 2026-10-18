from django.db import models
from django.db.models.functions import Lower


class CourseLevel(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    description = models.CharField(
        max_length=300,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "course_levels"
        ordering = ["name"]
        verbose_name = "Course Level"
        verbose_name_plural = "Course Levels"

        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="unique_course_level_name",
            ),
        ]

    def __str__(self):
        return self.name
