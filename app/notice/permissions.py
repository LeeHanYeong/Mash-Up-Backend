from rest_framework import permissions

__all__ = (
    'NoticeAuthorOnlyUpdateDestory',
    'AttendanceUserOnlyUpdate',
)


class NoticeAuthorOnlyUpdateDestory(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'PUT', 'DELETE'):
            return obj.author == request.user


class AttendanceUserOnlyUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'PUT'):
            return obj.user == request.user
        return False
