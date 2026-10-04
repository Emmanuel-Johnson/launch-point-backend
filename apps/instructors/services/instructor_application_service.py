from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from apps.instructors.models import InstructorApplication
from apps.instructors.repositories.instructor_application_repository import (
    InstructorApplicationRepository,
)


class InstructorApplicationService:
    @staticmethod
    def create_application(user, application_data):
        if not application_data.get("terms_accepted"):
            raise ValidationError(
                {"terms_accepted": "You must accept the terms and conditions."}
            )

        if InstructorApplication.objects.filter(
            user=user,
            status=InstructorApplication.Status.PENDING,
        ).exists():
            raise ValidationError(
                {"detail": "You already have a pending instructor application."}
            )

        try:
            with transaction.atomic():
                application_data["user"] = user

                return InstructorApplicationRepository.create_application(
                    application_data
                )

        except IntegrityError as exc:
            raise ValidationError(
                {"detail": "You already have a pending or approved application."}
            ) from exc
