from django.contrib import admin

from ..models import (
    Team,
    Period,
    UserPeriodTeam,
    UserPeriodOutcount,
)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_current')


@admin.register(UserPeriodTeam)
class UserPeriodTeamAdmin(admin.ModelAdmin):
    list_display = ('user', 'period', 'team')
    list_filter = ('period', 'team')
    search_fields = ('user__name',)


@admin.register(UserPeriodOutcount)
class UserPeriodOutcountAdmin(admin.ModelAdmin):
    list_display = ('user', 'period', 'count')
    list_filter = ('period',)
    list_editable = ('count',)
    search_fields = ('user__name',)
