from rest_framework import serializers

from notice.models import Notice
from utils.drf.serializers import ModelSerializer

__all__ = ("NoticePushSerializer",)


class NoticePushSerializer(ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="name", read_only=True)
    is_voted = serializers.IntegerField(help_text="투표에 참여한 인원 수", default=None)

    class Meta:
        model = Notice
        fields = (
            "id",
            "author",
            "start_at",
            "duration",
            "address1",
            "address2",
            "is_voted",
        )
