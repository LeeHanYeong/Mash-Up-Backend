import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import F, Count, Q, OuterRef, Exists
from django_extensions.db.models import TimeStampedModel
from push_notifications.models import Device, GCMDevice, APNSDevice
from safedelete.models import SafeDeleteModel
from simple_history.models import HistoricalRecords

from members.models import Team
from utils.django.fields import ChoiceField
from utils.django.models import Model

logger = logging.getLogger(__name__)
User = get_user_model()

__all__ = (
    "Notice",
    "Attendance",
)


class NoticeQuerySet(models.QuerySet):
    def with_voted(self, user):
        if user.is_authenticated:
            is_voted = Attendance.objects.filter(
                notice=OuterRef("id"), user=user,
            ).exclude(vote=Attendance.VOTE_UNSELECTED)
            return self.annotate(is_voted=Exists(is_voted))
        return self

    def with_count(self):
        return self.annotate(
            attendance_voted_count=Count(
                "attendance_set",
                filter=~Q(attendance_set__vote=Attendance.VOTE_UNSELECTED),
            ),
            attendance_count=Count("attendance_set"),
        )

    def with_attendance_set(self):
        return self.prefetch_related(
            "attendance_set",
            "attendance_set__user",
            "attendance_set__user__user_period_team_set",
        )


class NoticeManager(models.Manager):
    ORDERING = F("start_at").desc(nulls_last=True), "-id"

    def get_queryset(self):
        return (
            NoticeQuerySet(self.model, using=self._db)
            .select_related("author", "team",)
            .prefetch_related("author__user_period_team_set",)
            .order_by(*self.ORDERING)
        )

    def with_voted(self, user):
        return self.get_queryset().with_voted(user).order_by(*self.ORDERING)

    def with_count(self):
        return self.get_queryset().with_count().order_by(*self.ORDERING)

    def with_attendance_set(self):
        return self.get_queryset().with_attendance_set()().order_by(*self.ORDERING)


class Notice(Model):
    _history = HistoricalRecords(table_name="_history_notice")

    TYPE_ALL, TYPE_TEAM, TYPE_PROJECT = ("all", "team", "project")
    TYPE_CHOICES = (
        (TYPE_ALL, "전체 공지"),
        (TYPE_TEAM, "팀별 공지"),
        (TYPE_PROJECT, "프로젝트 공지"),
    )
    period = models.ForeignKey(
        "members.Period",
        verbose_name="해당 기수",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    type = ChoiceField("공지유형", choices=TYPE_CHOICES, max_length=10)
    team = models.ForeignKey(
        Team,
        verbose_name="팀",
        on_delete=models.CASCADE,
        related_name="notice_set",
        blank=True,
        null=True,
    )
    title = models.CharField("공지명", max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="작성자",
        on_delete=models.SET_NULL,
        related_name="notice_set",
        null=True,
    )
    start_at = models.DateTimeField("일시", blank=True, null=True)
    duration = models.DurationField("예상 진행시간", blank=True, null=True)
    address1 = models.CharField("주소", max_length=200, help_text="도로명/지번 주소", blank=True)
    address2 = models.CharField(
        "상세주소", max_length=100, help_text="건물명/층/호수/상세장소 등", blank=True
    )
    description = models.TextField("설명", blank=True)

    user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="투표할 사용자 목록",
        through="Attendance",
        through_fields=("notice", "user"),
        related_name="user_notice_set",
        blank=True,
    )

    objects = NoticeManager()

    class Meta:
        verbose_name = "공지"
        verbose_name_plural = f"{verbose_name} 목록"
        indexes = [
            models.Index(fields=["start_at"]),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        if self.type == self.TYPE_TEAM:
            if self.team is None:
                raise ValidationError("팀별 공지인 경우, 해당 팀을 선택해야 합니다")

    def save(self, **kwargs):
        print(self.type)
        self.clean()
        super().save()

    def add_attendance_set(self):
        q = Q(user_period_team__period=self.period)
        if self.team:
            q = q & Q(user_period_team__team=self.team)
        users = User.objects.filter(q)

        with transaction.atomic():
            for user in users:
                self.attendance_set.get_or_create(user=user)


class AttendanceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("notice", "user",)


class Attendance(Model):
    _history = HistoricalRecords(table_name="_history_attendance")

    VOTE_UNSELECTED, VOTE_ATTEND, VOTE_ABSENT, VOTE_LATE = (
        "unselected",
        "attend",
        "absent",
        "late",
    )
    CHOICES_VOTE = (
        (VOTE_UNSELECTED, "미선택"),
        (VOTE_ATTEND, "참여"),
        (VOTE_ABSENT, "미참여"),
        (VOTE_LATE, "지각"),
    )
    notice = models.ForeignKey(
        Notice,
        verbose_name="공지",
        on_delete=models.CASCADE,
        related_name="attendance_set",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="사용자",
        on_delete=models.CASCADE,
        related_name="attendance_set",
    )
    vote = ChoiceField(
        "투표", choices=CHOICES_VOTE, max_length=15, default=VOTE_UNSELECTED
    )
    result = models.CharField(
        "실제 참석결과", choices=CHOICES_VOTE, max_length=15, blank=True
    )

    objects = AttendanceManager()

    class Meta:
        verbose_name = "공지 참석 투표"
        verbose_name_plural = f"{verbose_name} 목록"
        unique_together = (("notice", "user"),)

    def __str__(self):
        return "{notice_title} ({user}, {vote})".format(
            notice_title=self.notice.title,
            user=self.user.name,
            vote=self.get_vote_display(),
        )
