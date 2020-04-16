from rest_framework import permissions

__all__ = (
    'NoticeAuthorOnlyUpdateDestroy',
    'AttendanceUserOnlyUpdate',
)


class NoticeAuthorOnlyUpdateDestroy(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'PUT', 'DELETE'):
            return obj.author == request.user
        return True


class AttendanceUserOnlyUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'PUT'):
            return obj.user == request.user
        return False
