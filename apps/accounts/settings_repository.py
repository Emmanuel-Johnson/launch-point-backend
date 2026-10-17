class SettingsRepository:
    @staticmethod
    def update_password(user, new_password):
        user.set_password(new_password)
        user.save(update_fields=["password", "updated_at"])
