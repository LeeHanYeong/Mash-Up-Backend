from django.contrib import admin

__all__ = (
    'StudyAdmin',
    'StudyMembershipAdmin',
)


class StudyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'period',
        'get_team_display',
        'get_members_display',
    )

    def get_team_display(self, obj):
        return ', '.join(list(obj.team_set.values_list('name', flat=True)))

    def get_members_display(self, obj):
        return ', '.join(
            [f'{member.last_name}{member.first_name}'
             for member in obj.members.values_list('last_name', 'first_name', named=True)]
        )

    get_members_display.short_description = '스터디원 목록'


class StudyMembershipAdmin(admin.ModelAdmin):
    list_display = (
        'study',
        'user',
        'late_fine',
    )
