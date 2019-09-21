from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_auth.views import LoginView
from rest_framework import generics, status

from .filters import UserFilterSet
from .models import Team, User, Period
from .serializers import UserSerializer, TeamSerializer, PeriodSerializer, AuthTokenSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Team List',
        operation_description='팀 목록 (ex: 백엔드, iOS....)'
    )
)
class TeamListAPIView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Period List',
        operation_description='기수 목록 (ex: 8기, 7기....)'
    )
)
class PeriodListAPIView(generics.ListAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='User List',
        operation_description='유저 목록'
    )
)
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilterSet


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='AuthToken',
        operation_description='인증정보를 사용해 사용자의 Token(key)과 User정보를 획득',
        responses={
            status.HTTP_200_OK: AuthTokenSerializer(),
        }
    ),
)
class AuthTokenAPIView(LoginView):
    def get_response_serializer(self):
        return AuthTokenSerializer
