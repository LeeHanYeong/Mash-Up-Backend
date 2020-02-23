from django.apps import AppConfig


class NoticeConfig(AppConfig):
    name = 'notice'
    verbose_name = '공지'

    def ready(self):
        import notice.signals  # noqa F401
