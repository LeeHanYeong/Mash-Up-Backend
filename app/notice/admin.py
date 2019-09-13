from django.contrib import admin

from .models import Notice, Attendance


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    inlines = [AttendanceInline]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    pass
