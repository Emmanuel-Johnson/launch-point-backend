import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdmin
from apps.core.responses import success_response
from apps.courses.models import Skill
from apps.courses.serializers.skill_serializer import (
    SkillCreateSerializer,
    SkillReadSerializer,
    SkillStatusSerializer,
    SkillUpdateSerializer,
)
from apps.courses.services.skill_service import SkillService

logger = logging.getLogger(__name__)


class SkillListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request: Request) -> Response:
        logger.info("Fetching all skills.")

        skills = SkillService.get_all_skills()
        serializer = SkillReadSerializer(skills, many=True)

        logger.info("Successfully fetched skills.")

        return success_response(
            message="Skills fetched successfully.",
            data=serializer.data,
        )

    def post(self, request: Request) -> Response:
        logger.info("Creating a new skill.")

        serializer = SkillCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        skill = SkillService.create_skill(
            **serializer.validated_data,
        )

        response_serializer = SkillReadSerializer(skill)

        logger.info(
            "Skill created successfully. ID: %s",
            skill.pk,
        )

        return success_response(
            message="Skill created successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


class SkillUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_skill(self, skill_id: int) -> Skill:
        try:
            return SkillService.get_skill_by_id(skill_id)
        except ObjectDoesNotExist:
            logger.warning(
                "Skill not found. ID: %s",
                skill_id,
            )
            raise NotFound("Skill not found.")

    def patch(self, request: Request, pk: int) -> Response:
        logger.info("Updating skill. ID: %s", pk)

        skill = self.get_skill(pk)

        serializer = SkillUpdateSerializer(
            instance=skill,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        updated_skill = SkillService.update_skill(
            skill,
            **serializer.validated_data,
        )

        response_serializer = SkillReadSerializer(updated_skill)

        logger.info(
            "Skill updated successfully. ID: %s",
            updated_skill.pk,
        )

        return success_response(
            message="Skill updated successfully.",
            data=response_serializer.data,
        )


class SkillStatusView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_skill(self, skill_id: int) -> Skill:
        try:
            return SkillService.get_skill_by_id(skill_id)
        except ObjectDoesNotExist:
            logger.warning(
                "Skill not found. ID: %s",
                skill_id,
            )
            raise NotFound("Skill not found.")

    def patch(self, request: Request, pk: int) -> Response:
        logger.info("Updating skill status. ID: %s", pk)

        skill = self.get_skill(pk)

        serializer = SkillStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_skill = SkillService.update_skill_status(
            skill=skill,
            **serializer.validated_data,
        )

        response_serializer = SkillReadSerializer(updated_skill)

        logger.info(
            "Skill status updated successfully. ID: %s",
            updated_skill.pk,
        )

        return success_response(
            message="Skill status updated successfully.",
            data=response_serializer.data,
        )


class SkillDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request: Request, pk: int) -> Response:
        logger.info("Soft-deleting skill. ID: %s", pk)

        try:
            skill = SkillService.get_skill_by_id(pk)
        except ObjectDoesNotExist:
            logger.warning(
                "Skill not found for deletion. ID: %s",
                pk,
            )
            raise NotFound("Skill not found.")

        SkillService.soft_delete_skill(skill)

        logger.info(
            "Skill soft-deleted successfully. ID: %s",
            pk,
        )

        return success_response(
            message="Skill deleted successfully.",
            data=None,
        )
