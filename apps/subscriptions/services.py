from apps.subscriptions.repositories import SubscriptionPlanRepository


class SubscriptionPlanService:
    @staticmethod
    def get_all_plans():
        return SubscriptionPlanRepository.get_all()

    @staticmethod
    def get_active_plans():
        return SubscriptionPlanRepository.get_active_plans()

    @staticmethod
    def get_plan_by_id(plan_id):
        return SubscriptionPlanRepository.get_by_id(plan_id)

    @staticmethod
    def create_plan(plan_data):
        return SubscriptionPlanRepository.create(plan_data)

    @staticmethod
    def update_plan(plan, plan_data):
        return SubscriptionPlanRepository.update(
            plan,
            plan_data,
        )

    @staticmethod
    def update_plan_status(plan, is_active):
        return SubscriptionPlanRepository.update_status(
            plan,
            is_active,
        )
