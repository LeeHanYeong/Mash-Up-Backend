from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter

from utils.drf.doc import schema
from . import apis

app_name = 'notices'

router = SimpleRouter()
router.register(r'', schema(
    apis.NoticeViewSet, (
        ('list', {
            'operation_description': '공지사항 목록',
        }),
        ('create', {
            'operation_description': '공지사항 생성',
        }),
        ('retrieve', {
            'operation_description': '공지사항 상세',
        }),
        ('update', {
            'operation_description': '공지사항 수정',
        }),
        ('destroy', {
            'operation_description': '공지사항 삭제',
        }),
    ),
))
DOC_ATTENDANCE_UPDATE = '''
**공지참여 투표 수정**

두 가지 방법으로 사용 가능
- Attendance기반으로 요청
    - URL: `/notices/attendances/<id>/` 에 요청
    - 이 경우, noticeId를 요청하지 않아도 됨
- Notice기반으로 요청
    - URL: `/notices/attendances/`
    - 이 경우, 반드시 noticeId를 request body에 담아 보내야 함
    - 해당 Notice에서 요청한 사용자의 투표현황을 수정함
'''

urlpatterns = [
    path('', include(router.urls)),
    # id가 optional
    re_path(r'attendances/(?:(?P<id>\d+)/)?$', schema(
        apis.AttendanceViewSet, (
            ('update', {
                'operation_description': DOC_ATTENDANCE_UPDATE,
            }),
        )).as_view({'patch': 'partial_update'})),
]
