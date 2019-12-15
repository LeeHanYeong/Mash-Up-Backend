from django.http import Http404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404

from .models import Notice, Attendance
from .permissions import NoticeAuthorOrReadOnly, AttendanceUserOrReadOnly
from .serializers import NoticeSerializer, NoticeCreateUpdateSerializer, AttendanceUpdateSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Notice List',
        operation_description='공지사항 목록'
    )
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='Notice Create',
        operation_description='공지사항 생성',
        responses={
            status.HTTP_200_OK: NoticeSerializer(),
        }
    )
)
class NoticeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return NoticeSerializer
        elif self.request.method == 'POST':
            return NoticeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Notice Retrieve',
        operation_description='공지사항 상세'
    )
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_summary='Notice Update',
        operation_description='공지사항 수정',
        responses={
            status.HTTP_200_OK: NoticeSerializer(),
        }
    )
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        operation_summary='Notice Destroy',
        operation_description='공지사항 삭제',
    ),
)
class NoticeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    permission_classes = (
        NoticeAuthorOrReadOnly,
    )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return NoticeSerializer
        elif self.request.method in ('PATCH', 'PUT'):
            return NoticeCreateUpdateSerializer

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)


@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_summary='Attendance Update',
        operation_description='''
**공지참여 투표 수정**

두 가지 방법으로 사용 가능
- Attendance기반으로 요청
    - URL: `/notices/attendances/<pk>/` 에 요청
    - 이 경우, noticePk를 요청하지 않아도 됨
- Notice기반으로 요청
    - URL: `/notices/attendances/`
    - 이 경우, 반드시 noticePk를 request body에 담아 보내야 함
    - 해당 Notice에서 요청한 사용자의 투표현황을 수정함
        ''',
    )
)
class AttendanceUpdateAPIView(generics.UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceUpdateSerializer
    permission_classes = (AttendanceUserOrReadOnly,)

    def get_object(self):
        try:
            attendance = super().get_object()
        except (AssertionError, Http404):
            notice_pk = self.request.data.get('notice_pk')
            notice = get_object_or_404(Notice, pk=notice_pk)
            attendance = notice.attendance_set.get(user=self.request.user)
        return attendance

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)
