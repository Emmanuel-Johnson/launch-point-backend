from rest_framework import serializers

from apps.instructors.models import InstructorApplication


class AdminInstructorApplicationListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    categories = serializers.SerializerMethodField()
    years_of_experience = serializers.SerializerMethodField()

    class Meta:
        model = InstructorApplication
        fields = (
            "id",
            "full_name",
            "email",
            "occupation",
            "years_of_experience",
            "status",
            "submitted_at",
            "categories",
        )

    def get_categories(self, obj):
        return list(obj.categories_to_teach.values_list("name", flat=True))

    def get_years_of_experience(self, obj):
        return obj.get_years_of_experience_display()
