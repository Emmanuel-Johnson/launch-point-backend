from django.urls import path

from apps.subscriptions.views import (
    AdminSubscriptionPlanDetailView,
    AdminSubscriptionPlanListCreateView,
    AdminSubscriptionPlanStatusView,
)

urlpatterns = [
    path(
        "plans/",
        AdminSubscriptionPlanListCreateView.as_view(),
        name="admin-subscription-plan-list-create",
    ),
    path(
        "plans/<int:plan_id>/",
        AdminSubscriptionPlanDetailView.as_view(),
        name="admin-subscription-plan-detail",
    ),
    path(
        "plans/<int:plan_id>/status/",
        AdminSubscriptionPlanStatusView.as_view(),
        name="admin-subscription-plan-status",
    ),
]
