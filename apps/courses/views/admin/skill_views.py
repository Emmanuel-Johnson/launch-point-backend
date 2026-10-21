from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdmin
from apps.courses.models import Skill
from apps.courses.serializers.skill_serializer import (
    CourseSkillSerializer,
    CourseSkillStatusSerializer,
)
from apps.courses.services.skill_service import (
    CourseSkillService,
)


class CourseSkillListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request: Request) -> Response:
        skills = CourseSkillService.get_all_skills()
        serializer = CourseSkillSerializer(skills, many=True)

        return Response(
            {
                "success": True,
                "message": "Skills retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        serializer = CourseSkillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        skill: Skill = CourseSkillService.create_skill(
            name=serializer.validated_data["name"],
            description=serializer.validated_data.get("description", ""),
        )

        return Response(
            {
                "success": True,
                "message": "Skill created successfully.",
                "data": CourseSkillSerializer(skill).data,
            },
            status=status.HTTP_201_CREATED,
        )


class CourseSkillUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(
        self,
        request: Request,
        skill_id: int,
    ) -> Response:
        skill = CourseSkillService.get_skill_by_id(
            skill_id=skill_id,
        )

        serializer = CourseSkillSerializer(
            skill,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        skill = CourseSkillService.update_skill_by_id(
            skill=skill,
            **serializer.validated_data,
        )

        return Response(
            {
                "success": True,
                "message": "Skill updated successfully.",
                "data": CourseSkillSerializer(skill).data,
            },
            status=status.HTTP_200_OK,
        )


class CourseSkillToggleStatusView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(
        self,
        request: Request,
        skill_id: int,
    ) -> Response:
        skill = CourseSkillService.get_skill_by_id(
            skill_id=skill_id,
        )

        serializer = CourseSkillStatusSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        skill = CourseSkillService.update_skill_status_by_id(
            skill=skill,
            is_active=serializer.validated_data["is_active"],
        )

        return Response(
            {
                "success": True,
                "message": "Skill status updated successfully.",
                "data": CourseSkillSerializer(skill).data,
            },
            status=status.HTTP_200_OK,
        )
