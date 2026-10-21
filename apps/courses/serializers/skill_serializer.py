from rest_framework import serializers

from apps.courses.models import Skill


class SkillBaseSerializer(serializers.ModelSerializer):
    def validate_name(self, value: str) -> str:
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Name must contain at least 3 characters."
            )

        queryset = Skill.objects.filter(
            name__iexact=value,
            is_deleted=False,
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("A skill with this name already exists.")

        return value


class SkillReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]


class SkillCreateSerializer(SkillBaseSerializer):
    class Meta:
        model = Skill
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


class SkillUpdateSerializer(SkillBaseSerializer):
    class Meta:
        model = Skill
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


class SkillStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()
