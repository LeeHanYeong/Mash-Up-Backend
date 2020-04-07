from rest_framework import permissions

__all__ = (
    'NoticeAuthorOnlyUpdate',
    'AttendanceUserOrReadOnly',
)


class NoticeAuthorOnlyUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'PUT', 'DELETE'):
            return obj.author == request.user


class AttendanceUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
