from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Count, Q, OuterRef, Exists
from django_extensions.db.models import TimeStampedModel
from members.models import Team
from utils.django.fields import ChoiceField
from utils.django.models import Model

User = get_user_model()


class NoticeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'author',
            'team',
        ).prefetch_related(
            'author__user_period_team_set',
            'attendance_set',
            'attendance_set__user',
            'attendance_set__user__user_period_team_set',
        )

    def with_count(self, user=None):
        qs = self.get_queryset().annotate(
            attendance_voted_count=Count(
                'attendance_set',
                filter=~Q(
                    attendance_set__vote=Attendance.VOTE_UNSELECTED
                )
            ),
            attendance_count=Count('attendance_set'),
        )
        if user:
            is_voted = Attendance.objects.filter(
                notice=OuterRef('pk'),
                user=user,
            ).exclude(vote=Attendance.VOTE_UNSELECTED)
            qs = qs.annotate(is_voted=Exists(is_voted))
        return qs


class Notice(TimeStampedModel, Model):
    TYPE_ALL, TYPE_TEAM, TYPE_PROJECT = ('all', 'team', 'project')
    TYPE_CHOICES = (
        (TYPE_ALL, '전체 공지'),
        (TYPE_TEAM, '팀별 공지'),
        (TYPE_PROJECT, '프로젝트 공지'),
    )
    type = ChoiceField('공지유형', choices=TYPE_CHOICES, max_length=10)
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
        ordering = (F('start_at').desc(nulls_last=True), '-pk')

    def __str__(self):
        return self.title

    def clean(self):
        if self.type == self.TYPE_TEAM:
            if self.team is None:
                raise ValidationError('팀별 공지인 경우, 해당 팀을 선택해야 합니다')

    def save(self, **kwargs):
        self.clean()
        super().save()


class AttendanceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'notice',
            'user',
        )


class Attendance(Model):
    VOTE_UNSELECTED, VOTE_ATTEND, VOTE_ABSENT, VOTE_LATE = 'unselected', 'attend', 'absent', 'late'
    CHOICES_VOTE = (
        (VOTE_UNSELECTED, '미선택'),
        (VOTE_ATTEND, '참여'),
        (VOTE_ABSENT, '미참여'),
        (VOTE_LATE, '지각'),
    )
    notice = models.ForeignKey(Notice, verbose_name='공지', on_delete=models.CASCADE, related_name='attendance_set')
    user = models.ForeignKey(User, verbose_name='사용자', on_delete=models.CASCADE, related_name='attendance_set')
    vote = ChoiceField('투표', choices=CHOICES_VOTE, max_length=15, default=VOTE_UNSELECTED)
    result = models.CharField('실제 참석결과', choices=CHOICES_VOTE, max_length=15, blank=True)

    objects = AttendanceManager()

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
