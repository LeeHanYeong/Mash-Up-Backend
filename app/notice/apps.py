import os

from django.apps import AppConfig


class NoticeConfig(AppConfig):
    name = "notice"
    verbose_name = "공지"

    def ready(self):
        if os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.production":
            import notice.signals  # noqa F401
