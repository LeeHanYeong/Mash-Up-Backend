from django_filters import rest_framework as filters

from .models import User


class UserFilterSet(filters.FilterSet):
    period = filters.CharFilter(method='filter_period')
    team = filters.CharFilter(method='filter_team')

    class Meta:
        model = User
        fields = (
            'period',
            'team',
        )

    def filter_period(self, queryset, name, value):
        return queryset._next_is_sticky().filter(
            user_period_team__period=value,
        )._next_is_sticky().distinct()

    def filter_team(self, queryset, name, value):
        return queryset._next_is_sticky().filter(
            user_period_team__team=value,
        )._next_is_sticky().distinct()
