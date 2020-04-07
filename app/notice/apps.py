import os

from django.apps import AppConfig


class NoticeConfig(AppConfig):
    name = 'notice'
    verbose_name = '공지'

    def ready(self):
        SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
        if SETTINGS_MODULE not in (
                'config.settings',
                'config.settings.local',
                'config.settings.dev',
                'config.settings.ci'):
            import notice.signals  # noqa F401
