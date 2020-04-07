from django_filters import rest_framework as filters

from .models import User


class UserFilterSet(filters.FilterSet):
    period = filters.NumberFilter(
        field_name='user_period_team__period', distinct=True,
        help_text='기수(Period) id',
    )
    team = filters.NumberFilter(
        field_name='user_period_team__team', distinct=True,
        help_text='팀(Team) id'
    )

    class Meta:
        model = User
        fields = (
            'period',
            'team',
        )

    # def filter_period(self, queryset, name, value):
    #     # return queryset._next_is_sticky().filter(
    #     #     user_period_team__period=value,
    #     # )._next_is_sticky().distinct()
    #     return queryset.filter(user_period_team__period=value).distinct()
    #
    # def filter_team(self, queryset, name, value):
    #     # return queryset._next_is_sticky().filter(
    #     #     user_period_team__team=value,
    #     # )._next_is_sticky().distinct()
    #     return queryset.filter(user_period_team__team=value).distinct()
