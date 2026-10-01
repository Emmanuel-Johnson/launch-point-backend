from rest_framework import serializers

from apps.subscriptions.models import SubscriptionPlan


class SubscriptionPlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan

        fields = [
            "id",
            "name",
            "plan_type",
            "price",
            "billing_interval",
            "is_active",
        ]


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan

        fields = [
            "id",
            "name",
            "plan_type",
            "description",
            "benefits",
            "price",
            "billing_interval",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_plan_type(self, value):
        if value == SubscriptionPlan.PlanType.FREE:
            queryset = SubscriptionPlan.objects.filter(
                plan_type=SubscriptionPlan.PlanType.FREE
            )

            # Exclude the current plan when editing
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError(
                    "A free subscription plan already exists."
                )

        return value

    def validate_benefits(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Benefits must be a list.")

        normalized_benefits = []

        for benefit in value:
            if not isinstance(benefit, str):
                raise serializers.ValidationError("Each benefit must be a string.")

            benefit = benefit.strip()

            if not benefit:
                raise serializers.ValidationError(
                    "Benefits cannot contain empty values."
                )

            normalized_benefits.append(benefit.lower())

        if len(normalized_benefits) != len(set(normalized_benefits)):
            raise serializers.ValidationError(
                "Benefits must not contain duplicate values."
            )

        return value
