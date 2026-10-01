from django.urls import path

from apps.subscriptions.views import StudentSubscriptionPlanListView

urlpatterns = [
    path(
        "plans/",
        StudentSubscriptionPlanListView.as_view(),
        name="student-subscription-plan-list",
    ),
]
