from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.categories.serializers import CategorySerializer
from apps.categories.services import CategoryService


class AdminCategoryListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        categories = CategoryService.get_all_categories()

        serializer = CategorySerializer(
            categories,
            many=True,
        )

        return Response(serializer.data)


class AdminCategoryDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, category_id):
        category = CategoryService.get_category_by_id(category_id)

        if not category:
            return Response(
                {"detail": "Category not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CategorySerializer(category)

        return Response(serializer.data)


class AdminCategoryStatusView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, category_id):
        is_active = request.data.get("is_active")

        if not isinstance(is_active, bool):
            return Response(
                {"detail": "is_active must be a boolean."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        category = CategoryService.get_category_by_id(category_id)

        if not category:
            return Response(
                {"detail": "Category not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        category = CategoryService.set_category_status(
            category=category,
            is_active=is_active,
        )

        message = (
            "Category activated successfully."
            if category.is_active
            else "Category deactivated successfully."
        )

        return Response(
            {
                "is_active": category.is_active,
                "message": message,
            }
        )


class AdminCategoryUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, category_id):
        category = CategoryService.get_category_by_id(category_id)

        if not category:
            return Response(
                {"detail": "Category not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        category = CategoryService.update_category(
            category,
            **serializer.validated_data,
        )

        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_200_OK,
        )
