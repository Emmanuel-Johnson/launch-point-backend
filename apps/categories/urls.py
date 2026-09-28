from django.urls import path

from apps.categories.views import (
    AdminCategoryDetailView,
    AdminCategoryListView,
    AdminCategoryStatusView,
    AdminCategoryUpdateView,
)

urlpatterns = [
    path(
        "categories/",
        AdminCategoryListView.as_view(),
        name="admin-category-list",
    ),
    path(
        "categories/<int:category_id>/",
        AdminCategoryDetailView.as_view(),
        name="admin-category-detail",
    ),
    path(
        "categories/<int:category_id>/status/",
        AdminCategoryStatusView.as_view(),
        name="admin-category-status",
    ),
    path(
        "categories/<int:category_id>/update/",
        AdminCategoryUpdateView.as_view(),
        name="admin-category-update",
    ),
]
