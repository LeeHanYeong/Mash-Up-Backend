from django.contrib import admin


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PeriodAdmin(admin.ModelAdmin):
    list_display = ('number',)


class UserPeriodTeamAdmin(admin.ModelAdmin):
    list_display = ('user', 'period', 'team')
    list_filter = ('period', 'team')
    search_fields = ('user__name',)
