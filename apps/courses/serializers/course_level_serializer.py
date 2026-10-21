from rest_framework import serializers

from apps.courses.models import CourseLevel


class CourseLevelBaseSerializer(serializers.ModelSerializer):
    def validate_name(self, value: str) -> str:
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Name must contain at least 3 characters."
            )

        queryset = CourseLevel.objects.filter(
            name__iexact=value,
            is_deleted=False,
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A course level with this name already exists."
            )

        return value


class CourseLevelReadSerializer(serializers.ModelSerializer):
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


class CourseLevelCreateSerializer(CourseLevelBaseSerializer):
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


class CourseLevelUpdateSerializer(CourseLevelBaseSerializer):
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
            "is_active",
            "created_at",
            "updated_at",
        ]


class CourseLevelStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()
