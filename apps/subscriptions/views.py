from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.subscriptions.serializers import (
    SubscriptionPlanListSerializer,
    SubscriptionPlanSerializer,
)
from apps.subscriptions.services import SubscriptionPlanService


class AdminSubscriptionPlanListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        plans = SubscriptionPlanService.get_all_plans()

        serializer = SubscriptionPlanListSerializer(
            plans,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = SubscriptionPlanSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        plan = SubscriptionPlanService.create_plan(
            serializer.validated_data,
        )

        return Response(
            SubscriptionPlanSerializer(plan).data,
            status=status.HTTP_201_CREATED,
        )


class AdminSubscriptionPlanDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, plan_id):
        plan = SubscriptionPlanService.get_plan_by_id(plan_id)

        serializer = SubscriptionPlanSerializer(plan)

        return Response(serializer.data)

    def patch(self, request, plan_id):
        plan = SubscriptionPlanService.get_plan_by_id(plan_id)

        serializer = SubscriptionPlanSerializer(
            plan,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        plan = SubscriptionPlanService.update_plan(
            plan,
            serializer.validated_data,
        )

        return Response(
            SubscriptionPlanSerializer(plan).data,
        )


class AdminSubscriptionPlanStatusView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, plan_id):
        plan = SubscriptionPlanService.get_plan_by_id(plan_id)

        is_active = request.data.get("is_active")

        if not isinstance(is_active, bool):
            return Response(
                {"detail": "is_active must be a boolean."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        plan = SubscriptionPlanService.update_plan_status(
            plan,
            is_active,
        )

        return Response(
            SubscriptionPlanSerializer(plan).data,
        )
