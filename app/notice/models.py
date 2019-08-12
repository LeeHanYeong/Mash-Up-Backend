from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel
from members.models import Team

User = get_user_model()


class Notice(TimeStampedModel):
    team = models.ForeignKey(
        Team, verbose_name='팀', on_delete=models.CASCADE,
        related_name='notice_set', blank=True, null=True,
    )
    title = models.CharField('공지명')
    author = models.ForeignKey(
        User, verbose_name='작성자', on_delete=models.SET_NULL,
        related_name='notice_set', null=True,
    )
    start_at = models.DateTimeField('일시', blank=True, null=True, db_index=True)
    duration = models.DurationField('예상 진행시간', blank=True, null=True)
    address1 = models.CharField('주소', max_length=200, help_text='도로명/지번 주소', blank=True)
    address2 = models.CharField('상세주소', max_length=100, help_text='건물명/층/호수/상세장소 등', blank=True)
    description = models.TextField('설명', blank=True)

    class Meta:
        verbose_name = '공지'
        verbose_name_plural = f'{verbose_name} 목록'


class NoticeVote(models.Model):
    pass
