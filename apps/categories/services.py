from apps.categories.repositories import CategoryRepository


class CategoryService:
    @staticmethod
    def get_all_categories():
        return CategoryRepository.get_all_categories()

    @staticmethod
    def get_active_categories():
        return CategoryRepository.get_active_categories()

    @staticmethod
    def get_category_by_id(category_id):
        return CategoryRepository.get_category_by_id(category_id)

    @staticmethod
    def get_category_by_slug(slug):
        return CategoryRepository.get_category_by_slug(slug)

    @staticmethod
    def create_category(**data):
        return CategoryRepository.create_category(**data)

    @staticmethod
    def update_category(category, **data):
        return CategoryRepository.update_category(category, **data)

    @staticmethod
    def set_category_status(category, is_active):
        return CategoryRepository.update_category_status(
            category,
            is_active,
        )
