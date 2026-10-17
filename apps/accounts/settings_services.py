from apps.accounts.settings_repository import SettingsRepository


class SettingsService:
    @staticmethod
    def change_password(user, new_password):
        SettingsRepository.update_password(
            user=user,
            new_password=new_password,
        )
