import uuid

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """
    Manager for the custom User model, which authenticates by email
    instead of a username.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and persist a User with a hashed password.

        Raises:
            ValueError: If email or password is not provided.
        """
        if not email:
            raise ValueError("Email is required")

        if not password:
            raise ValueError("Password is required")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and persist a superuser.

        Defaults is_staff, is_superuser, and is_active to True, and requires
        is_staff and is_superuser to be True.

        Raises:
            ValueError: If is_staff or is_superuser is not True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", self.model.Role.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom authentication user keyed by email address.

    Uses email as the login identifier (USERNAME_FIELD) rather than a
    username. Accounts may authenticate via password or be linked to a
    Google account through google_id.
    """

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        INSTRUCTOR = "instructor", "Instructor"
        ADMIN = "admin", "Admin"

    full_name = models.CharField(max_length=150)

    email = models.EmailField(unique=True, max_length=255)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    # Set when the account is linked to a Google (OAuth) identity; null for
    # accounts that authenticate with a password only.
    google_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )

    email_verified = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class EmailVerificationOTP(models.Model):
    """
    Hashed one-time password used to verify a user's email address.

    Only the OTP hash is stored (never the raw code), and expires_at bounds
    how long the OTP remains valid.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_verification_otps",
    )

    otp_hash = models.CharField(max_length=128)

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "email_verification_otps"

    def __str__(self):
        return f"Email verification OTP - {self.user.email}"


class PasswordResetOTP(models.Model):
    """
    Hashed one-time password used to authorize a password-reset request.

    Only the OTP hash is stored (never the raw code), and expires_at bounds
    how long the OTP remains valid.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_otps",
    )

    otp_hash = models.CharField(max_length=128)

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "password_reset_otps"


class PasswordResetToken(models.Model):
    """
    Single-use, hashed token issued after a password-reset OTP is verified.

    The token authorizes the final password-reset step. Only the token hash
    is stored (never the raw token); expires_at bounds its validity and
    used_at records when it was consumed.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
    )

    token_hash = models.CharField(
        max_length=64,
        unique=True,
    )

    expires_at = models.DateTimeField()

    # Null while the token is still valid; set once the token has been
    # consumed to enforce single use.
    used_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        default=timezone.now,
    )

    class Meta:
        db_table = "password_reset_tokens"

    def __str__(self):
        return f"Password reset token - {self.user.email}"


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
