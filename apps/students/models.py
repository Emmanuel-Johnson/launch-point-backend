from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    """
    Stores profile and educational information specific to a student.

    Each student has one profile associated with their user account.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    profile_image = models.ImageField(
        upload_to="student_profiles/",
        null=True,
        blank=True,
    )

    bio = models.TextField(
        blank=True,
        max_length=500,
    )

    location = models.CharField(
        max_length=150,
        blank=True,
    )

    education = models.CharField(
        max_length=150,
        blank=True,
    )

    occupation = models.CharField(
        max_length=150,
        blank=True,
    )

    github_url = models.URLField(
        max_length=255,
        blank=True,
    )

    linkedin_url = models.URLField(
        max_length=255,
        blank=True,
    )

    portfolio_url = models.URLField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "student_profiles"

    def __str__(self):
        return f"Student Profile - {self.user.email}"
