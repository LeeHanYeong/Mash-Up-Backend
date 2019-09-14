from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status

from .models import Notice
from .permissions import NoticeAuthorOrReadOnly
from .serializers import NoticeSerializer, NoticeCreateUpdateSerializer


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