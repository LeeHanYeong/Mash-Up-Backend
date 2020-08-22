from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

from members.models import Period, Team
from utils.django.models import Model

__all__ = (
    "Study",
    "StudyMeeting",
    "StudyMeetingFine",
    "StudyMeetingFineCategory",
    "StudyMeetingUserActivity",
    "StudyMembership",
)


class Study(TimeStampedModel):
    period = models.ForeignKey(
        Period,
        verbose_name="기수",
        on_delete=models.PROTECT,
        related_name="study_set",
        related_query_name="study",
    )
    team_set = models.ManyToManyField(
        Team, verbose_name="팀 목록", related_name="study_set", related_query_name="study",
    )
    name = models.CharField("스터디명", max_length=100)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="스터디원 목록",
        blank=True,
        through="StudyMembership",
        related_name="study_set",
        related_query_name="study",
    )

    class Meta:
        verbose_name = "스터디"
        verbose_name_plural = f"{verbose_name} 목록"
        ordering = ("-id",)

    def __str__(self):
        return self.name


class StudyMembership(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="스터디원",
        on_delete=models.CASCADE,
        related_name="membership_set",
        related_query_name="membership",
    )
    study = models.ForeignKey(
        Study,
        verbose_name="스터디",
        on_delete=models.CASCADE,
        related_name="membership_set",
        related_query_name="membership",
    )
    late_fine = models.PositiveIntegerField("벌금", default=0)

    class Meta:
        verbose_name = "스터디원 정보"
        verbose_name_plural = f"{verbose_name} 목록"

    def __str__(self):
        return f"{self.study.name} | 유저({self.user.name})"


class StudyMeeting(TimeStampedModel):
    study = models.ForeignKey(
        Study,
        verbose_name="스터디",
        on_delete=models.PROTECT,
        related_name="meeting_set",
        related_query_name="meeting",
    )
    start_at = models.DateTimeField("시작일시")
    end_at = models.DateTimeField("종료일시")
    location = models.CharField("장소", max_length=200)

    class Meta:
        verbose_name = "스터디모임"
        verbose_name_plural = f"{verbose_name} 목록"

    def __str__(self):
        return "{study} | 모임 (회차: {number}, 일시: {start} ~ {end})".format(
            study=self.study.name,
            number=self.number,
            start=self.start_at,
            end=self.end_at,
        )

    @property
    def number(self):
        return self.study.meeting_set.filter(id__lte=self.id).count()


class StudyMeetingUserActivity(Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="스터디원",
        on_delete=models.PROTECT,
        related_name="meeting_user_activity_set",
        related_query_name="meeting_user_activity",
    )
    meeting = models.ForeignKey(
        StudyMeeting,
        verbose_name="스터디 모임",
        on_delete=models.PROTECT,
        related_name="meeting_user_activity_set",
        related_query_name="meeting_user_activity",
    )

    class Meta:
        verbose_name = "스터디모임 유저활동정보"
        verbose_name_plural = f"{verbose_name} 목록"

    def __str__(self):
        return "{study} | 활동정보 (회차: {number}, 구성원: {user})".format(
            study=self.meeting.study.name,
            number=self.meeting.number,
            user=self.user.name,
        )


class StudyMeetingFineCategory(Model):
    name = models.CharField("벌금 카테고리명", max_length=100)

    class Meta:
        verbose_name = "스터디모임 벌금 카테고리"
        verbose_name_plural = f"{verbose_name} 목록"

    def __str__(self):
        return self.name


class StudyMeetingFine(Model):
    meeting_user_activity = models.ForeignKey(
        StudyMeetingUserActivity,
        verbose_name="스터디 모임 활동정보",
        on_delete=models.CASCADE,
        related_name="fine_set",
        related_query_name="fine",
    )
    category = models.ForeignKey(
        StudyMeetingFineCategory,
        verbose_name="카테고리",
        on_delete=models.PROTECT,
        related_name="fine_set",
        related_query_name="fine",
    )
    amount = models.PositiveIntegerField("금액")

    class Meta:
        verbose_name = "스터디모임 벌금"
        verbose_name_plural = f"{verbose_name} 목록"

    def __str__(self):
        return "{study} | 벌금 (사유: {category}, 회차: {number}, 구성원: {user}, 금액: {amount}".format(
            study=self.meeting_user_activity.meeting.study.name,
            number=self.meeting_user_activity.meeting.number,
            user=self.meeting_user_activity.user.name,
            category=self.category.name,
            amount=self.amount,
        )
