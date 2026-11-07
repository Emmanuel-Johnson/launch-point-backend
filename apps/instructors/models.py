from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Q


class InstructorApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="instructor_applications",
    )

    full_name = models.CharField(
        max_length=150,
        default="Unknown",
    )

    profile_image = models.ImageField(
        upload_to="instructor_applications/profile_images/",
        null=True,
        blank=True,
    )

    # Professional information submitted for review
    occupation = models.CharField(max_length=150, blank=True)
    education = models.CharField(max_length=200, blank=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    experience_months = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(11)],
    )
    categories_to_teach = models.ManyToManyField(
        "categories.Category",
        related_name="instructor_applications",
        blank=True,
    )
    professional_bio = models.TextField(max_length=1000)

    # Contact and professional links submitted with the application
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=150, blank=True)
    linkedin_url = models.URLField(max_length=255, blank=True)
    github_url = models.URLField(max_length=255, blank=True)
    portfolio_url = models.URLField(max_length=255, blank=True)

    # Application-only information
    motivation = models.TextField(max_length=1000)
    resume = models.FileField(
        upload_to="instructor_applications/resumes/",
    )

    terms_accepted = models.BooleanField(default=False)

    # Administrative review
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    admin_message = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_instructor_applications",
    )

    is_dashboard_opened = models.BooleanField(default=False)

    class Meta:
        db_table = "instructor_applications"
        ordering = ["-submitted_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(status="pending"),
                name="unique_pending_instructor_application_per_user",
            ),
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(status="approved"),
                name="unique_approved_instructor_application_per_user",
            ),
            models.CheckConstraint(
                condition=Q(experience_months__gte=0, experience_months__lte=11),
                name="valid_instructor_experience_months",
            ),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.status}"


class InstructorApplicationDocument(models.Model):
    application = models.ForeignKey(
        InstructorApplication,
        on_delete=models.CASCADE,
        related_name="supporting_documents",
    )

    document = models.FileField(
        upload_to="instructor_applications/documents/",
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "instructor_application_documents"
        ordering = ["uploaded_at"]

    def __str__(self):
        return f"Supporting document - {self.application.user.email}"


class InstructorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="instructor_profile",
    )

    is_active = models.BooleanField(default=True)

    # Instructor identity
    full_name = models.CharField(
        max_length=150,
        default="Unknown",
    )

    profile_image = models.ImageField(
        upload_to="instructor_profiles/",
        null=True,
        blank=True,
    )

    # Instructor-specific public profile
    occupation = models.CharField(max_length=150, blank=True)
    professional_bio = models.TextField(max_length=1000, blank=True)
    education = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=150, blank=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    experience_months = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(11)],
    )
    # Date the instructor application was submitted
    application_submitted_at = models.DateTimeField(null=True, blank=True)

    # Set when the application is approved
    became_instructor_at = models.DateTimeField(null=True, blank=True)

    categories_to_teach = models.ManyToManyField(
        "categories.Category",
        related_name="instructor_profiles",
        blank=True,
    )

    # Instructor-specific professional links
    linkedin_url = models.URLField(max_length=255, blank=True)
    github_url = models.URLField(max_length=255, blank=True)
    portfolio_url = models.URLField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "instructor_profiles"
        constraints = [
            models.CheckConstraint(
                condition=Q(experience_months__gte=0, experience_months__lte=11),
                name="valid_profile_experience_months",
            )
        ]

    def __str__(self):
        return f"Instructor Profile - {self.full_name}"
