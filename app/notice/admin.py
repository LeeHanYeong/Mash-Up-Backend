from django.contrib import admin
from django.contrib.auth import get_user_model
from safedelete.admin import SafeDeleteAdmin, highlight_deleted
from simple_history.admin import SimpleHistoryAdmin

from .models import Notice, Attendance

User = get_user_model()


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1
    readonly_fields = ('user',)
    exclude = ('_history_user',)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'user':
            choices = getattr(request, '_user_choices_cache', None)
            if choices is None:
                request._user_choices_cache = choices = list(formfield.choices)
            formfield.choices = formfield.choices
        return formfield


@admin.register(Notice)
class NoticeAdmin(SafeDeleteAdmin, SimpleHistoryAdmin):
    list_display = (highlight_deleted, 'title', 'type', 'team', 'author', 'start_at', 'duration', 'address1', 'address2')
    list_filter = ('type', 'team') + SafeDeleteAdmin.list_filter
    inlines = [AttendanceInline]
    readonly_fields = ('_history_user',)
    exclude = ('_history_user',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['queryset'] = User.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Attendance)
class AttendanceAdmin(SimpleHistoryAdmin):
    list_display = ('notice', 'user', 'vote', 'result')
    list_filter = ('vote', 'result')
    search_fields = ('notice__title', 'user__name')
