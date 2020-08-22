from django.core.management import BaseCommand
from push_notifications.models import GCMDevice

from notice.models import Notice
from notice.serializers import NoticeSerializer
from utils.push import case


class Command(BaseCommand):
    def handle(self, *args, **options):
        notice = Notice.objects.order_by("-pk").first()
        gcm_devices = GCMDevice.objects.filter(user__user_notice_set=notice)
        message = f'"{notice.title}" 공지가 등록되었습니다'
        extra = {
            "case": case.NOTICE_CREATED,
            "data": NoticeSerializer(notice).data,
        }
        gcm_devices.send_message(message, extra=extra)
