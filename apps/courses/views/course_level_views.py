from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.courses.serializers.course_level_serializer import (
    CourseLevelCreateSerializer,
    CourseLevelReadSerializer,
    CourseLevelStatusSerializer,
    CourseLevelUpdateSerializer,
)
from apps.courses.services.course_level_service import (
    CourseLevelService,
)


class CourseLevelListCreateView(APIView):
    def get(self, request):
        levels = CourseLevelService.get_all_levels()

        serializer = CourseLevelReadSerializer(
            levels,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = CourseLevelCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        level = CourseLevelService.create_level(**serializer.validated_data)

        response_serializer = CourseLevelReadSerializer(level)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class CourseLevelUpdateView(APIView):
    def patch(self, request, pk):
        try:
            level = CourseLevelService.get_level_by_id(pk)
        except ObjectDoesNotExist:
            raise NotFound("Course level not found.")

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

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )


class CourseLevelStatusView(APIView):
    def patch(self, request, pk):
        try:
            level = CourseLevelService.get_level_by_id(pk)
        except ObjectDoesNotExist:
            raise NotFound("Course level not found.")

        serializer = CourseLevelStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_level = CourseLevelService.update_level_status(
            level=level,
            **serializer.validated_data,
        )

        response_serializer = CourseLevelReadSerializer(updated_level)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
