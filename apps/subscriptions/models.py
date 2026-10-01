from django.conf import settings
from django.db import models


class SubscriptionPlan(models.Model):
    class PlanType(models.TextChoices):
        FREE = "free", "Free"
        PREMIUM = "premium", "Premium"

    class BillingInterval(models.TextChoices):
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"
        YEARLY = "yearly", "Yearly"

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    plan_type = models.CharField(
        max_length=20,
        choices=PlanType.choices,
    )

    description = models.TextField()

    benefits = models.JSONField(default=list)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    billing_interval = models.CharField(
        max_length=20,
        choices=BillingInterval.choices,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "subscription_plans"
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["plan_type"],
                condition=models.Q(plan_type="free"),
                name="unique_free_plan_type",
            ),
        ]

    def __str__(self):
        return self.name


class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name="subscriptions",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    start_date = models.DateTimeField()

    end_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "subscriptions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.plan}"
