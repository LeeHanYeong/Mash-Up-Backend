from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty

from members.serializers import TeamSerializer, UserSerializer
from ..models import Notice, Attendance

User = get_user_model()


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
    OPTIONAL_FIELDS = (
        'attendance_voted_count',
        'attendance_count',
        'is_voted',
    )
    type_display = serializers.CharField(source='get_type_display')
    team = TeamSerializer()
    author = UserSerializer()

    attendance_set = _NoticeAttendanceSerializer(many=True, help_text='투표현황 목록')
    attendance_voted_count = serializers.IntegerField(help_text='투표에 참여한 인원 수')
    attendance_count = serializers.IntegerField(help_text='투표 가능한 총 인원 수')
    is_voted = serializers.NullBooleanField(help_text='사용자의 투표여부', default=None)

    def __init__(self, instance=None, data=empty, **kwargs):
        for optional_field in self.OPTIONAL_FIELDS:
            if not hasattr(instance, optional_field):
                self.fields.pop(optional_field)
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = Notice
        fields = (
            'pk',
            'type',
            'type_display',
            'team',
            'title',
            'author',
            'start_at',
            'duration',
            'address1',
            'address2',
            'description',

            'attendance_set',
            'attendance_voted_count',
            'attendance_count',
            'is_voted',
        )


class NoticeCreateUpdateSerializer(serializers.ModelSerializer):
    user_pk_list = serializers.ListField(
        child=serializers.IntegerField(), write_only=True,
        help_text='이 공지사항에 참석여부 투표할 사용자 PK List'
    )

    class Meta:
        model = Notice
        fields = (
            'type',
            'team',
            'title',
            'start_at',
            'duration',
            'address1',
            'address2',
            'description',

            'user_pk_list',
        )

    def __init__(self, *args, **kwargs):
        # user_pk_list내부의 값이 int가 아닌 dict(JSON object)로 온 경우, 이를 pk로 변환
        if 'data' in kwargs:
            data_user_pk_list = kwargs['data'].get('user_pk_list')
            for index, data_user_pk in enumerate(data_user_pk_list):
                if isinstance(data_user_pk, dict):
                    kwargs['data']['user_pk_list'][index] = data_user_pk['pk']

            data_author = kwargs['data'].get('author')
            if isinstance(data_author, dict):
                kwargs['data']['author'] = kwargs['data'].pop('author')['pk']
        super().__init__(*args, **kwargs)

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
            Attendance.objects.bulk_create(
                [Attendance(notice=notice, user=user) for user in users])
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
            Attendance.objects.bulk_create(
                [Attendance(notice=notice, user=user)
                 for user in create_users]
            )
            return notice

    def to_representation(self, instance):
        # attendance_voted_count항목의 annotate처리
        instance = Notice.objects.with_count().get(pk=instance.pk)
        return NoticeSerializer(instance).data
