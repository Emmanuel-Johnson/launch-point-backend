import logging

from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.subscriptions.serializers import (
    StudentSubscriptionPlanSerializer,
    SubscriptionPlanListSerializer,
    SubscriptionPlanSerializer,
)
from apps.subscriptions.services import SubscriptionPlanService

logger = logging.getLogger(__name__)


class AdminSubscriptionPlanListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logger.info(
            "Admin requested subscription plan list.",
            extra={"user_id": request.user.id},
        )

        plans = SubscriptionPlanService.get_all_plans()

        serializer = SubscriptionPlanListSerializer(
            plans,
            many=True,
        )

        logger.info(
            "Subscription plan list returned successfully.",
            extra={"user_id": request.user.id, "count": len(serializer.data)},
        )

        return Response(serializer.data)

    def post(self, request):
        logger.info(
            "Admin requested subscription plan creation.",
            extra={"user_id": request.user.id},
        )

        serializer = SubscriptionPlanSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        plan = SubscriptionPlanService.create_plan(
            serializer.validated_data,
        )

        logger.info(
            "Subscription plan created successfully.",
            extra={"user_id": request.user.id, "plan_id": plan.id},
        )

        return Response(
            SubscriptionPlanSerializer(plan).data,
            status=status.HTTP_201_CREATED,
        )


class AdminSubscriptionPlanDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, plan_id):
        logger.info(
            "Admin requested subscription plan detail.",
            extra={"user_id": request.user.id, "plan_id": plan_id},
        )

        plan = SubscriptionPlanService.get_plan_by_id(plan_id)

        serializer = SubscriptionPlanSerializer(plan)

        logger.info(
            "Subscription plan detail returned successfully.",
            extra={"user_id": request.user.id, "plan_id": plan_id},
        )

        return Response(serializer.data)

    def patch(self, request, plan_id):
        logger.info(
            "Admin requested subscription plan update.",
            extra={"user_id": request.user.id, "plan_id": plan_id},
        )

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

        logger.info(
            "Subscription plan updated successfully.",
            extra={"user_id": request.user.id, "plan_id": plan_id},
        )

        return Response(
            SubscriptionPlanSerializer(plan).data,
        )


class AdminSubscriptionPlanStatusView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, plan_id):
        logger.info(
            "Admin requested subscription plan status update.",
            extra={"user_id": request.user.id, "plan_id": plan_id},
        )

        plan = SubscriptionPlanService.get_plan_by_id(plan_id)

        is_active = request.data.get("is_active")

        if not isinstance(is_active, bool):
            logger.warning(
                "Subscription plan status update rejected: "
                "is_active must be a boolean.",
                extra={"user_id": request.user.id, "plan_id": plan_id},
            )
            return Response(
                {"detail": "is_active must be a boolean."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        plan = SubscriptionPlanService.update_plan_status(
            plan,
            is_active,
        )

        logger.info(
            "Subscription plan status updated successfully.",
            extra={
                "user_id": request.user.id,
                "plan_id": plan_id,
                "is_active": plan.is_active,
            },
        )

        return Response(
            SubscriptionPlanSerializer(plan).data,
        )


class StudentSubscriptionPlanListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(
            "Student requested active subscription plan list.",
            extra={"user_id": request.user.id},
        )

        plans = SubscriptionPlanService.get_active_plans()

        serializer = StudentSubscriptionPlanSerializer(
            plans,
            many=True,
        )

        logger.info(
            "Active subscription plan list returned successfully.",
            extra={"user_id": request.user.id, "count": len(serializer.data)},
        )

        return Response(serializer.data)
