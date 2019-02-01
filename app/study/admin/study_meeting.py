from django.contrib import admin

__all__ = (
    'StudyMeetingAdmin',
    'StudyMeetingUserActivityAdmin',
    'StudyMeetingFineCategoryAdmin',
    'StudyMeetingFineAdmin',
)


class StudyMeetingAdmin(admin.ModelAdmin):
    list_display = ('study', 'location')

    def get_datetime_display(self, obj):
        return f'{obj.start_at} ~ {obj.end_at}'


class StudyMeetingUserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'meeting')


class StudyMeetingFineCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class StudyMeetingFineAdmin(admin.ModelAdmin):
    list_display = ('meeting_user_activity', 'category')
