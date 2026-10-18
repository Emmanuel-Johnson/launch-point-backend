from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdmin
from apps.courses.models import CourseLevel
from apps.courses.serializers.course_level_serializer import (
    CourseLevelSerializer,
    CourseLevelStatusSerializer,
)
from apps.courses.services.course_level_service import (
    CourseLevelService,
)


class CourseLevelListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request: Request) -> Response:
        levels = CourseLevelService.get_all_levels()
        serializer = CourseLevelSerializer(levels, many=True)

        return Response(
            {
                "success": True,
                "message": "Course levels retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        serializer = CourseLevelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        level: CourseLevel = CourseLevelService.create_level(
            name=serializer.validated_data["name"],
            description=serializer.validated_data.get("description", ""),
        )

        return Response(
            {
                "success": True,
                "message": "Course level created successfully.",
                "data": CourseLevelSerializer(level).data,
            },
            status=status.HTTP_201_CREATED,
        )


class CourseLevelUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(
        self,
        request: Request,
        level_id: int,
    ) -> Response:
        level = CourseLevelService.get_level_by_id(
            level_id=level_id,
        )

        serializer = CourseLevelSerializer(
            level,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        level = CourseLevelService.update_level_by_id(
            level=level,
            **serializer.validated_data,
        )

        return Response(
            {
                "success": True,
                "message": "Course level updated successfully.",
                "data": CourseLevelSerializer(level).data,
            },
            status=status.HTTP_200_OK,
        )


class CourseLevelToggleStatusView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(
        self,
        request: Request,
        level_id: int,
    ) -> Response:
        level = CourseLevelService.get_level_by_id(
            level_id=level_id,
        )

        serializer = CourseLevelStatusSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        level = CourseLevelService.update_level_status_by_id(
            level=level,
            is_active=serializer.validated_data["is_active"],
        )

        return Response(
            {
                "success": True,
                "message": "Course level status updated successfully.",
                "data": CourseLevelSerializer(level).data,
            },
            status=status.HTTP_200_OK,
        )
