from django.utils import timezone

from apps.instructors.models import InstructorApplication, InstructorProfile


class InstructorApplicationRepository:
    @staticmethod
    def get_all_applications():
        return (
            InstructorApplication.objects.select_related("user")
            .prefetch_related("categories_to_teach")
            .order_by("-submitted_at")
        )

    @staticmethod
    def get_application_by_id(application_id):
        return (
            InstructorApplication.objects.select_related(
                "user",
                "reviewed_by",
            )
            .prefetch_related(
                "categories_to_teach",
                "supporting_documents",
            )
            .filter(id=application_id)
            .first()
        )

    @staticmethod
    def reject_application(application, admin, admin_message):
        application.status = InstructorApplication.Status.REJECTED
        application.admin_message = admin_message
        application.reviewed_at = timezone.now()
        application.reviewed_by = admin

        application.save(
            update_fields=[
                "status",
                "admin_message",
                "reviewed_at",
                "reviewed_by",
                "updated_at",
            ]
        )

        return application

    @staticmethod
    def get_application_for_rejection(application_id):
        return InstructorApplication.objects.filter(id=application_id).first()

    @staticmethod
    def approve_application(application, admin, admin_message):
        application.status = InstructorApplication.Status.APPROVED
        application.admin_message = admin_message
        application.reviewed_at = timezone.now()
        application.reviewed_by = admin

        application.save(
            update_fields=[
                "status",
                "admin_message",
                "reviewed_at",
                "reviewed_by",
                "updated_at",
            ]
        )

        return application

    @staticmethod
    def get_application_for_approval(application_id):
        return InstructorApplication.objects.filter(id=application_id).first()

    @staticmethod
    def create_instructor_profile_from_application(application):
        profile, created = InstructorProfile.objects.get_or_create(
            user=application.user,
            defaults={
                "full_name": application.full_name,
                "profile_image": (
                    application.profile_image.name
                    if application.profile_image
                    else None
                ),
                "occupation": application.occupation,
                "professional_bio": application.professional_bio,
                "education": application.education,
                "location": application.location,
                "years_of_experience": application.years_of_experience,
                "linkedin_url": application.linkedin_url,
                "github_url": application.github_url,
                "portfolio_url": application.portfolio_url,
                "became_instructor_at": application.reviewed_at,
            },
        )

        if created:
            profile.categories_to_teach.set(application.categories_to_teach.all())

        return profile

    @staticmethod
    def update_user_role(user, role):
        user.role = role
        user.save(update_fields=["role", "updated_at"])
        return user
