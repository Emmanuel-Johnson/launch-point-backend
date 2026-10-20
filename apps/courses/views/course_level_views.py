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
from apps.courses.models import CourseLevel
from apps.courses.serializers.course_level_serializer import (
    CourseLevelCreateSerializer,
    CourseLevelReadSerializer,
    CourseLevelStatusSerializer,
    CourseLevelUpdateSerializer,
)
from apps.courses.services.course_level_service import CourseLevelService

logger = logging.getLogger(__name__)


class CourseLevelListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request: Request) -> Response:
        logger.info("Fetching all course levels.")

        levels = CourseLevelService.get_all_levels()
        serializer = CourseLevelReadSerializer(levels, many=True)

        logger.info("Successfully fetched course levels.")

        return success_response(
            message="Course levels fetched successfully.",
            data=serializer.data,
        )

    def post(self, request: Request) -> Response:
        logger.info("Creating a new course level.")

        serializer = CourseLevelCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        level = CourseLevelService.create_level(
            **serializer.validated_data,
        )

        response_serializer = CourseLevelReadSerializer(level)

        logger.info(
            "Course level created successfully. ID: %s",
            level.pk,
        )

        return success_response(
            message="Course level created successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


class CourseLevelUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_level(self, level_id: int) -> CourseLevel:
        try:
            return CourseLevelService.get_level_by_id(level_id)
        except ObjectDoesNotExist:
            logger.warning(
                "Course level not found. ID: %s",
                level_id,
            )
            raise NotFound("Course level not found.")

    def patch(self, request: Request, pk: int) -> Response:
        logger.info("Updating course level. ID: %s", pk)

        level = self.get_level(pk)

        serializer = CourseLevelUpdateSerializer(
            instance=level,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        updated_level = CourseLevelService.update_level(
            level,
            **serializer.validated_data,
        )

        response_serializer = CourseLevelReadSerializer(updated_level)

        logger.info(
            "Course level updated successfully. ID: %s",
            updated_level.pk,
        )

        return success_response(
            message="Course level updated successfully.",
            data=response_serializer.data,
        )


class CourseLevelStatusView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_level(self, level_id: int) -> CourseLevel:
        try:
            return CourseLevelService.get_level_by_id(level_id)
        except ObjectDoesNotExist:
            logger.warning(
                "Course level not found. ID: %s",
                level_id,
            )
            raise NotFound("Course level not found.")

    def patch(self, request: Request, pk: int) -> Response:
        logger.info("Updating course level status. ID: %s", pk)

        level = self.get_level(pk)

        serializer = CourseLevelStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_level = CourseLevelService.update_level_status(
            level=level,
            **serializer.validated_data,
        )

        response_serializer = CourseLevelReadSerializer(updated_level)

        logger.info(
            "Course level status updated successfully. ID: %s",
            updated_level.pk,
        )

        return success_response(
            message="Course level status updated successfully.",
            data=response_serializer.data,
        )
