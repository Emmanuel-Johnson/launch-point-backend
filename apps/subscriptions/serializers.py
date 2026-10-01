from decimal import Decimal

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

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Plan name cannot be empty.")

        if len(value) < 3:
            raise serializers.ValidationError(
                "Plan name must be at least 3 characters long."
            )

        if len(value) > 100:
            raise serializers.ValidationError("Plan name cannot exceed 100 characters.")

        return value

    def validate_description(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Description cannot be empty.")

        if len(value) < 10:
            raise serializers.ValidationError(
                "Description must be at least 10 characters long."
            )

        if len(value) > 500:
            raise serializers.ValidationError(
                "Description cannot exceed 500 characters."
            )

        return value

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

    def validate_price(self, value):
        if value < Decimal("0.00"):
            raise serializers.ValidationError("Price cannot be negative.")

        if value > Decimal("999999.99"):
            raise serializers.ValidationError("Price cannot exceed 999999.99.")

        return value

    def validate_benefits(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Benefits must be a list.")

        # Minimum 3 benefits
        if len(value) < 3:
            raise serializers.ValidationError(
                "A subscription plan must have at least 3 benefits."
            )

        # Maximum 25 benefits
        if len(value) > 25:
            raise serializers.ValidationError(
                "A subscription plan can have a maximum of 25 benefits."
            )

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

        # Case-insensitive duplicate check
        if len(normalized_benefits) != len(set(normalized_benefits)):
            raise serializers.ValidationError(
                "Benefits must not contain duplicate values."
            )

        return value


class StudentSubscriptionPlanSerializer(serializers.ModelSerializer):
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
        ]
