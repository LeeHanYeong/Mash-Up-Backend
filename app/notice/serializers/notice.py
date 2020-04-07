from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty

from members.serializers import TeamSerializer, UserSerializer
from utils.drf.serializers import ModelSerializer
from ..models import Notice, Attendance

User = get_user_model()


class _NoticeAttendanceSerializer(ModelSerializer):
    user = UserSerializer()
    vote_display = serializers.CharField(source='get_vote_display')

    class Meta:
        model = Attendance
        fields = (
            'id',
            'user',
            'vote',
            'vote_display',
        )


class NoticeSerializer(ModelSerializer):
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
            'id',
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


class NoticeCreateUpdateSerializer(ModelSerializer):
    user_id_list = serializers.ListField(
        child=serializers.IntegerField(), write_only=True,
        help_text='이 공지사항에 참석여부 투표할 사용자 ID List'
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

            'user_id_list',
        )

    def __init__(self, *args, **kwargs):
        # user_id_list내부의 값이 int가 아닌 dict(JSON object)로 온 경우, 이를 id로 변환
        if 'data' in kwargs:
            data_user_id_list = kwargs['data'].get('user_id_list')
            for index, data_user_id in enumerate(data_user_id_list):
                if isinstance(data_user_id, dict):
                    kwargs['data']['user_id_list'][index] = data_user_id['id']

            data_author = kwargs['data'].get('author')
            if isinstance(data_author, dict):
                kwargs['data']['author'] = kwargs['data'].pop('author')['id']
        super().__init__(*args, **kwargs)

    def validate_user_id_list(self, id_list):
        if User.objects.filter(id__in=id_list).count() != len(id_list):
            invalid_user_id_list = []
            for id in id_list:
                if not User.objects.filter(id=id).exists():
                    invalid_user_id_list.append(id)

            raise ValidationError('유효하지 않은 UserID가 존재합니다 ({id_list})'.format(
                id_list=', '.join(invalid_user_id_list),
            ))
        return id_list

    def create(self, validated_data):
        with transaction.atomic():
            user_id_list = validated_data.pop('user_id_list', [])
            notice = super().create(validated_data)
            users = User.objects.filter(id__in=user_id_list)
            Attendance.objects.bulk_create(
                [Attendance(notice=notice, user=user) for user in users])
            return notice

    def update(self, instance, validated_data):
        with transaction.atomic():
            user_id_list = validated_data.pop('user_id_list', [])
            notice = super().update(instance, validated_data)

            # 포함되지 않은 User들에 해당하는 Attendance들을 삭제
            notice.attendance_set.exclude(user__in=user_id_list).delete()

            # 새로 만들어야 할 Attendance User id list
            exists_user_id_list = notice.attendance_set.values_list('user', flat=True)
            create_user_id_list = [id for id in user_id_list if id not in exists_user_id_list]
            create_users = User.objects.filter(id__in=create_user_id_list)

            # 새 Attendance create
            Attendance.objects.bulk_create(
                [Attendance(notice=notice, user=user)
                 for user in create_users]
            )
            return notice

    def to_representation(self, instance):
        # attendance_voted_count항목의 annotate처리
        instance = Notice.objects.with_count().get(id=instance.id)
        return NoticeSerializer(instance).data
