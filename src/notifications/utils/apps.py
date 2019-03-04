from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = 'notifications.utils'

    def ready(self):
        from . import checks  # noqa
