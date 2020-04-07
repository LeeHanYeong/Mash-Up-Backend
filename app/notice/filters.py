from django_filters import rest_framework as filters

from .models import Notice

__all__ = (
    'NoticeFilter',
)


class NoticeFilter(filters.FilterSet):
    type = filters.CharFilter(
        help_text=Notice.choices_help_text(Notice.TYPE_CHOICES))

    class Meta:
        model = Notice
        fields = (
            'type',
        )
