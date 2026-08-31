from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "is_active",
        "is_staff",
        "date_joined",
    )

    search_fields = (
        "full_name",
        "email",
    )

    list_filter = (
        "is_active",
        "is_staff",
    )