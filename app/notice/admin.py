from django.contrib import admin

from .models import Notice, Attendance


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1
    readonly_fields = ('user',)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'user':
            formfield.choices = formfield.choices
        return formfield


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'team', 'author', 'start_at', 'duration', 'address1', 'address2')
    list_filter = ('type', 'team')
    inlines = [AttendanceInline]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('notice', 'user', 'vote', 'result')
    list_filter = ('vote', 'result')
    search_fields = ('notice__title', 'user__name')
