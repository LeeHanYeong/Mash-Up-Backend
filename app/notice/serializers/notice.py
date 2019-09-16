from django.db import transaction
from rest_framework import serializers

from members.serializers import TeamSerializer, UserSerializer
from utils.drf.exceptions import ValidationError
from ..models import Notice, User, Attendance


class _NoticeAttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    vote_display = serializers.CharField(source='get_vote_display')

    class Meta:
        model = Attendance
        fields = (
            'pk',
            'user',
            'vote',
            'vote_display',
        )


class NoticeSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    author = UserSerializer()

    attendance_set = _NoticeAttendanceSerializer(many=True, help_text='투표현황 목록')

    class Meta:
        model = Notice
        fields = (
            'pk',
            'team',
            'title',
            'author',
            'start_at',
            'duration',
            'address1',
            'address2',
            'description',

            'attendance_set',
        )


class NoticeCreateUpdateSerializer(serializers.ModelSerializer):
    user_pk_list = serializers.ListField(
        child=serializers.IntegerField(), write_only=True,
        help_text='이 공지사항에 참석여부 투표할 사용자 PK List'
    )

    class Meta:
        model = Notice
        fields = (
            'team',
            'title',
            'start_at',
            'duration',
            'address1',
            'address2',
            'description',

            'user_pk_list',
        )

    def validate_user_pk_list(self, pk_list):
        if User.objects.filter(pk__in=pk_list).count() != len(pk_list):
            invalid_user_pk_list = []
            for pk in pk_list:
                if not User.objects.filter(pk=pk).exists():
                    invalid_user_pk_list.append(pk)

            raise ValidationError('유효하지 않은 UserPK가 존재합니다 ({pk_list})'.format(
                pk_list=', '.join(invalid_user_pk_list),
            ))
        return pk_list

    def create(self, validated_data):
        with transaction.atomic():
            user_pk_list = validated_data.pop('user_pk_list', [])
            notice = super().create(validated_data)
            users = User.objects.filter(pk__in=user_pk_list)
            Attendance.objects.bulk_create([Attendance(notice=notice, user=user) for user in users])
            return notice

    def update(self, instance, validated_data):
        with transaction.atomic():
            user_pk_list = validated_data.pop('user_pk_list', [])
            notice = super().update(instance, validated_data)

            # 포함되지 않은 User들에 해당하는 Attendance들을 삭제
            notice.attendance_set.exclude(user__in=user_pk_list).delete()

            # 새로 만들어야 할 Attendance User pk list
            exists_user_pk_list = notice.attendance_set.values_list('user', flat=True)
            create_user_pk_list = [pk for pk in user_pk_list if pk not in exists_user_pk_list]
            create_users = User.objects.filter(pk__in=create_user_pk_list)

            # 새 Attendance create
            Attendance.objects.bulk_create([Attendance(notice=notice, user=user) for user in create_users])
            return notice

    def to_representation(self, instance):
        return NoticeSerializer(instance).data
