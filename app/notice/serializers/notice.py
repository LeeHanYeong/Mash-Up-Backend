from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty

from members.serializers import TeamSerializer, UserSerializer
from utils.drf.fields import PkModelField
from utils.drf.serializers import ModelSerializer, WritableNestedModelSerializer
from ..models import Notice, Attendance

User = get_user_model()

__all__ = (
    "NoticeSerializer",
    "NoticeDetailSerializer",
    "NoticeCreateUpdateSerializer",
)


class _NoticeAttendanceSerializer(ModelSerializer):
    user = UserSerializer()
    vote_display = serializers.CharField(source="get_vote_display")

    class Meta:
        model = Attendance
        fields = (
            "id",
            "user",
            "vote",
            "vote_display",
        )


class NoticeSerializer(ModelSerializer):
    type_display = serializers.CharField(source="get_type_display")
    team = TeamSerializer()
    author = UserSerializer()

    attendance_voted_count = serializers.IntegerField(
        help_text="투표에 참여한 인원 수", default=None
    )
    attendance_count = serializers.IntegerField(help_text="투표 가능한 총 인원 수", default=None)
    is_voted = serializers.BooleanField(help_text="투표 참여여부", default=None)
    vote = serializers.CharField(help_text="참여한 투표 상태", default=None)

    class Meta:
        model = Notice
        fields = (
            "id",
            "type",
            "type_display",
            "team",
            "title",
            "author",
            "start_at",
            "duration",
            "address1",
            "address2",
            "description",
            "attendance_voted_count",
            "attendance_count",
            "is_voted",
            "vote",
        )


class NoticeDetailSerializer(NoticeSerializer):
    attendance_set = _NoticeAttendanceSerializer(many=True, help_text="투표현황 목록")

    class Meta(NoticeSerializer.Meta):
        model = Notice
        fields = NoticeSerializer.Meta.fields + ("attendance_set",)


class NoticeCreateUpdateSerializer(WritableNestedModelSerializer):
    user_set = serializers.ListField(child=PkModelField(User))

    class Meta:
        model = Notice
        fields = (
            "type",
            "team",
            "title",
            "start_at",
            "duration",
            "address1",
            "address2",
            "description",
            "user_set",
        )

    def create(self, validated_data):
        user_set = validated_data.pop("user_set", [])
        notice = super().create(validated_data)
        Attendance.objects.bulk_create(
            [Attendance(notice=notice, user=user) for user in user_set]
        )
        return notice

    def update(self, instance, validated_data):
        user_set = validated_data.pop("user_set", [])
        notice = super().update(instance, validated_data)

        # 포함되지 않은 User들에 해당하는 Attendance들을 삭제
        notice.attendance_set.exclude(user__in=user_set).delete()

        # 새로 포함될 User는 create, 기존 유저는 get처리
        for user in user_set:
            notice.attendance_set.get_or_create(user=user)
        return notice

    def to_representation(self, instance):
        # attendance_voted_count항목의 annotate처리
        instance = Notice.objects.with_count().get(id=instance.id)
        return NoticeDetailSerializer(instance).data
