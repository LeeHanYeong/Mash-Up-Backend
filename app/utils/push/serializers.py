from rest_framework import serializers

from notice.models import Notice
from utils.drf.serializers import ModelSerializer

__all__ = (
    'NoticePushSerializer',
)


class NoticePushSerializer(ModelSerializer):
    author = serializers.SlugRelatedField('name')
    is_voted = serializers.SerializerMethodField(help_text='투표에 참여한 인원 수')

    class Meta:
        model = Notice
        fields = (
            'id',
            'author',
            'start_at',
            'duration',
            'address1',
            'address2',

            'is_voted',
        )

    def get_is_voted(self, obj):
        return getattr(obj, 'is_voted', None)
