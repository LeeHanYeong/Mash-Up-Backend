from django.urls import path, include, re_path
from rest_framework import status
from rest_framework.routers import SimpleRouter

from utils.drf.doc import schema
from . import apis
from .serializers import AuthTokenSerializer

app_name = 'members'

router = SimpleRouter()
router.register('teams', schema(
    apis.TeamViewSet, [
        ('list', {
            'operation_description': '팀 목록 (ex: 백엔드, iOS....)'
        }),
    ]))
router.register('periods', schema(
    apis.PeriodViewSet, [
        ('list', {
            'operation_description': '기수 목록 (ex: 8기, 7기....)',
        }),
    ]))
router.register('users', schema(
    apis.UserViewSet, [
        ('list', {
            'operation_description': '사용자 목록',
        }),
    ]))

urlpatterns = [
    path('profile/', schema(
        apis.ProfileViewSet, (
            ('retrieve', {
                'operation_description': '유저 프로필 (헤더에 토큰이 존재할 시, 토큰에 해당하는 유저정보 리턴)',
            }),
        )).as_view({'get': 'retrieve'})),
    path('auth-token/', schema(
        apis.AuthTokenAPIView, [
            ('post', {
                'operation_id': 'Get AuthToken',
                'operation_description': '인증정보를 사용해 사용자의 Token(key)과 User정보를 획득',
                'responses': {
                    status.HTTP_200_OK: AuthTokenSerializer(),
                }
            }),
        ]).as_view()),
    path('', include(router.urls)),
]
