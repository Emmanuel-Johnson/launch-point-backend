from apps.instructors.models import InstructorApplication


class InstructorApplicationRepository:
    @staticmethod
    def create_application(application_data):
        return InstructorApplication.objects.create(**application_data)
