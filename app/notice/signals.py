import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from push_notifications.models import GCMDevice

from utils.push import case
from .models import Notice

logger = logging.getLogger('signal')


@receiver(post_save, sender=Notice)
def notice_created(sender, instance, created, **kwargs):
    from .serializers import NoticeSerializer
    logger.info(f'notice_created (pk: {instance.pk})')
    gcm_devices = GCMDevice.objects.filter(user__user_notice_set=instance)
    message = f'"{instance.title}" 공지가 등록되었습니다'
    extra = {
        'case': case.NOTICE_CREATED,
        'data': NoticeSerializer(instance).data,
    }
    gcm_devices.send_message(message, extra=extra)
