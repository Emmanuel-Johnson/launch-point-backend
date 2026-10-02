import logging

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.categories.serializers import CategorySerializer
from apps.categories.services import CategoryService

logger = logging.getLogger(__name__)


class AdminCategoryListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logger.info(
            "Admin requested category list.",
            extra={"user_id": request.user.id},
        )

        categories = CategoryService.get_all_categories()

        serializer = CategorySerializer(
            categories,
            many=True,
        )

        logger.info(
            "Category list returned successfully.",
            extra={"user_id": request.user.id, "count": len(serializer.data)},
        )

        return Response(serializer.data)

    def post(self, request):
        logger.info(
            "Admin requested category creation.",
            extra={"user_id": request.user.id},
        )

        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = CategoryService.create_category(**serializer.validated_data)

        logger.info(
            "Category created successfully.",
            extra={"user_id": request.user.id, "category_id": category.id},
        )

        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED,
        )


class AdminCategoryDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, category_id):
        logger.info(
            "Admin requested category detail.",
            extra={"user_id": request.user.id, "category_id": category_id},
        )

        category = CategoryService.get_category_by_id(category_id)

        if not category:
            logger.warning(
                "Category not found.",
                extra={"user_id": request.user.id, "category_id": category_id},
            )
            return Response(
                {"detail": "Category not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CategorySerializer(category)

        logger.info(
            "Category detail returned successfully.",
            extra={"user_id": request.user.id, "category_id": category_id},
        )

        return Response(serializer.data)


class AdminCategoryStatusView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, category_id):
        logger.info(
            "Admin requested category status update.",
            extra={"user_id": request.user.id, "category_id": category_id},
        )

        is_active = request.data.get("is_active")

        if not isinstance(is_active, bool):
            logger.warning(
                "Category status update rejected: is_active must be a boolean.",
                extra={"user_id": request.user.id, "category_id": category_id},
            )
            return Response(
                {"detail": "is_active must be a boolean."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        category = CategoryService.get_category_by_id(category_id)

        if not category:
            logger.warning(
                "Category not found for status update.",
                extra={"user_id": request.user.id, "category_id": category_id},
            )
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

        logger.info(
            "Category status updated successfully.",
            extra={
                "user_id": request.user.id,
                "category_id": category_id,
                "is_active": category.is_active,
            },
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
        logger.info(
            "Admin requested category update.",
            extra={"user_id": request.user.id, "category_id": category_id},
        )

        category = CategoryService.get_category_by_id(category_id)

        if not category:
            logger.warning(
                "Category not found for update.",
                extra={"user_id": request.user.id, "category_id": category_id},
            )
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

        logger.info(
            "Category updated successfully.",
            extra={"user_id": request.user.id, "category_id": category_id},
        )

        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_200_OK,
        )
