from django.conf import settings
from django.db import models
from django.db.models import Q


class InstructorApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    class Experience(models.TextChoices):
        LESS_THAN_ONE = "less_than_one", "Less than 1 year"
        ONE_TO_THREE = "one_to_three", "1–3 years"
        THREE_TO_FIVE = "three_to_five", "3–5 years"
        FIVE_TO_TEN = "five_to_ten", "5–10 years"
        TEN_PLUS = "ten_plus", "10+ years"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="instructor_applications",
    )

    # Professional information submitted for review
    occupation = models.CharField(max_length=150, blank=True)
    education = models.CharField(max_length=200, blank=True)
    years_of_experience = models.CharField(
        max_length=20,
        choices=Experience.choices,
    )
    categories_to_teach = models.JSONField(default=list, blank=True)
    short_bio = models.TextField(max_length=1000)

    # Contact and professional links submitted with the application
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=150, blank=True)
    linkedin_url = models.URLField(max_length=255, blank=True)
    github_url = models.URLField(max_length=255, blank=True)
    portfolio_url = models.URLField(max_length=255, blank=True)

    # Application-only information
    motivation = models.TextField(max_length=2000)
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
    admin_message = models.TextField(blank=True)
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

    # Instructor-specific public profile
    occupation = models.CharField(max_length=150, blank=True)
    short_bio = models.TextField(max_length=1000, blank=True)
    education = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=150, blank=True)
    years_of_experience = models.CharField(
        max_length=20,
        choices=InstructorApplication.Experience.choices,
        blank=True,
    )
    categories_to_teach = models.JSONField(default=list, blank=True)

    # Instructor-specific professional links
    linkedin_url = models.URLField(max_length=255, blank=True)
    github_url = models.URLField(max_length=255, blank=True)
    portfolio_url = models.URLField(max_length=255, blank=True)

    # Set when the application is approved
    became_instructor_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "instructor_profiles"

    def __str__(self):
        return f"Instructor Profile - {self.user.email}"
