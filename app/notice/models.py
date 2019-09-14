from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel
from members.models import Team

User = get_user_model()


class NoticeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(

        ).prefetch_related(
            'user_set',
        )


class Notice(TimeStampedModel):
    team = models.ForeignKey(
        Team, verbose_name='팀', on_delete=models.CASCADE,
        related_name='notice_set', blank=True, null=True,
    )
    title = models.CharField('공지명', max_length=100)
    author = models.ForeignKey(
        User, verbose_name='작성자', on_delete=models.SET_NULL,
        related_name='notice_set', null=True,
    )
    start_at = models.DateTimeField('일시', blank=True, null=True, db_index=True)
    duration = models.DurationField('예상 진행시간', blank=True, null=True)
    address1 = models.CharField('주소', max_length=200, help_text='도로명/지번 주소', blank=True)
    address2 = models.CharField('상세주소', max_length=100, help_text='건물명/층/호수/상세장소 등', blank=True)
    description = models.TextField('설명', blank=True)

    user_set = models.ManyToManyField(
        User, verbose_name='투표할 사용자 목록',
        through='Attendance', related_name='user_notice_set', blank=True,
    )

    objects = NoticeManager()

    class Meta:
        verbose_name = '공지'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.title


class Attendance(models.Model):
    VOTE_UNSELECTED, VOTE_ATTEND, VOTE_ABSENT, VOTE_LATE = 'unselected', 'attend', 'absent', 'late'
    CHOICES_VOTE = (
        (VOTE_UNSELECTED, '미선택'),
        (VOTE_ATTEND, '참여'),
        (VOTE_ABSENT, '미참여'),
        (VOTE_LATE, '지각'),
    )
    notice = models.ForeignKey(Notice, verbose_name='공지', on_delete=models.CASCADE, related_name='attendance_set')
    user = models.ForeignKey(User, verbose_name='사용자', on_delete=models.CASCADE, related_name='attendance_set')
    vote = models.CharField('투표', choices=CHOICES_VOTE, max_length=15, default=VOTE_UNSELECTED)
    result = models.CharField('실제 참석결과', choices=CHOICES_VOTE, max_length=15, blank=True)

    class Meta:
        verbose_name = '공지 참석 투표'
        verbose_name_plural = f'{verbose_name} 목록'
        unique_together = (
            ('notice', 'user'),
        )

    def __str__(self):
        return '{notice_title} ({user}, {vote})'.format(
            notice_title=self.notice.title,
            user=self.user.name,
            vote=self.get_vote_display(),
        )
