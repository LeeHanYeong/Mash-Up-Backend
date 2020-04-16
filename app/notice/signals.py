import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from push_notifications.models import GCMDevice

from utils.push import case
from .models import Notice, Attendance

logger = logging.getLogger('signal')


@receiver(post_save, sender=Notice)
def notice_post_save(sender, instance, created, **kwargs):
    from utils.push.serializers import NoticePushSerializer
    logger.info(f'notice_created (id: {instance.id})')
    gcm_devices = GCMDevice.objects.filter(user__user_notice_set=instance)
    message = f'"{instance.title}" 공지가 {"등록" if created else "수정"}되었습니다'
    extra = {
        'case': case.NOTICE_CREATED if created else case.NOTICE_MODIFIED,
        'data': NoticePushSerializer(instance).data,
    }
    gcm_devices.send_message(message, extra=extra)


def notice_resend(instance):
    from utils.push.serializers import NoticePushSerializer
    # GCMDevice의 필터 기준으로 user를 사용
    # 사용자가 투표할 사용자로 포함된 Notice이며,
    #  사용자의 참석투표의 notice가 Notice이며
    #  동시에 참석투표가 'unselected'이어야 함 (이미 투표한 사람에겐 보내지 않음)
    gcm_devices = GCMDevice.objects.filter(
        # user와 MTM으로 연결된 Notice목록중, 현재 save된 Notice가 존재하며
        user__user_notice_set=instance,
        # 아래는 동시조건
        # - "user가 가진 참석투표"에 "연결된 notice"가 현재 save된 Notice이며
        # - "user가 가진 참석투표"의 "vote"가 미선택(unselected)인 경우
        user__attendance_set__notice=instance,
        user__attendance_set__vote=Attendance.VOTE_UNSELECTED,
    )
    message = f'"{instance.title}" 공지가 수정되었습니다'
    extra = {
        'case': case.NOTICE_MODIFIED,
        'data': NoticePushSerializer(instance).data,
    }
    gcm_devices.send_message(message, extra=extra)
