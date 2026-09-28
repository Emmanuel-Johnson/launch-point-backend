from apps.categories.models import Category


class CategoryRepository:
    """Repository for category database operations."""

    @staticmethod
    def get_all():
        return Category.objects.all()

    @staticmethod
    def get_active():
        return Category.objects.filter(is_active=True)

    @staticmethod
    def get_by_id(category_id):
        return Category.objects.filter(id=category_id).first()

    @staticmethod
    def get_by_slug(slug):
        return Category.objects.filter(slug=slug).first()

    @staticmethod
    def create(**data):
        return Category.objects.create(**data)

    @staticmethod
    def update(category, **data):
        for field, value in data.items():
            setattr(category, field, value)

        category.save()
        return category

    @staticmethod
    def set_active_status(category, is_active):
        category.is_active = is_active
        category.save(update_fields=["is_active", "updated_at"])
        return category
