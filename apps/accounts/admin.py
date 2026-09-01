from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

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
        "delete_user",
    )

    search_fields = (
        "full_name",
        "email",
    )

    list_filter = (
        "is_active",
        "is_staff",
    )

    @admin.display(description="Delete")
    def delete_user(self, obj):
        url = reverse(
            "admin:accounts_user_delete",
            args=[obj.pk],
        )

        return format_html(
            '<a href="{}" style="color: #ba2121;">Delete</a>',
            url,
        )