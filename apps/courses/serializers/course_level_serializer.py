from rest_framework import serializers

from apps.courses.models import CourseLevel


class CourseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLevel
        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value: str) -> str:
        name = value.strip()

        if not name:
            raise serializers.ValidationError("Course level name cannot be empty.")

        queryset = CourseLevel.objects.filter(name__iexact=name)

        # Exclude the current instance when updating.
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A course level with this name already exists."
            )

        return name


class CourseLevelStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()
