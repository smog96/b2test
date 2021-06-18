from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.core_app'
    label = 'core_app'
    verbose_name = 'Приложение'
