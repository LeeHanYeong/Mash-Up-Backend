from django.http import Http404
from rest_framework import permissions

from utils.drf.exceptions import get_object_or_exception
from utils.drf.viewsets import ModelViewSet, UpdateModelViewSet
from .exceptions import NoticeNotFound
from .filters import NoticeFilter
from .models import Notice, Attendance
from .permissions import NoticeAuthorOnlyUpdateDestroy, AttendanceUserOnlyUpdate
from .serializers import (
    NoticeSerializer,
    NoticeCreateUpdateSerializer,
    NoticeDetailSerializer,
    AttendanceUpdateSerializer,
)

__all__ = (
    'NoticeViewSet',
    'AttendanceViewSet',
)


class NoticeViewSet(ModelViewSet):
    queryset = Notice.objects.with_count()
    filterset_class = NoticeFilter
    permission_classes = (
        permissions.IsAuthenticated,
        NoticeAuthorOnlyUpdateDestroy,
    )
    serializer_classes = {
        'list': NoticeSerializer,
        'retrieve': NoticeDetailSerializer,
        'create': NoticeCreateUpdateSerializer,
        'update': NoticeCreateUpdateSerializer,
    }

    def get_queryset(self):
        qs = self.queryset.with_voted(user=self.request.user)
        if self.action == 'retrieve':
            qs = qs.with_attendance_set()
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AttendanceViewSet(UpdateModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceUpdateSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        AttendanceUserOnlyUpdate,
    )

    def get_object(self):
        try:
            attendance = super().get_object()
        except (Attendance.DoesNotExist, AssertionError, Http404):
            notice_id = self.request.data.get('notice_id')
            notice = get_object_or_exception(Notice, NoticeNotFound, id=notice_id)
            attendance = notice.attendance_set.get(user=self.request.user)
        return attendance
