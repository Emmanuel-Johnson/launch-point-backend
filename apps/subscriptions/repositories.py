from apps.subscriptions.models import SubscriptionPlan


class SubscriptionPlanRepository:
    @staticmethod
    def get_all():
        return SubscriptionPlan.objects.all()

    @staticmethod
    def get_active_plans():
        return SubscriptionPlan.objects.filter(is_active=True)

    @staticmethod
    def get_by_id(plan_id):
        return SubscriptionPlan.objects.get(id=plan_id)

    @staticmethod
    def create(plan_data):
        return SubscriptionPlan.objects.create(**plan_data)

    @staticmethod
    def update(plan, plan_data):
        for field, value in plan_data.items():
            setattr(plan, field, value)

        plan.save()

        return plan

    @staticmethod
    def update_status(plan, is_active):
        plan.is_active = is_active
        plan.save(update_fields=["is_active", "updated_at"])

        return plan
