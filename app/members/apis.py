from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_auth.views import LoginView
from rest_framework import status

from utils.drf.viewsets import ListModelViewSet, RetrieveModelViewSet
from .filters import UserFilterSet
from .models import Team, User, Period
from .serializers import UserSerializer, TeamSerializer, PeriodSerializer, AuthTokenSerializer

__all__ = (
    'TeamViewSet',
    'PeriodViewSet',
    'UserViewSet',
    'ProfileViewSet',
    'AuthTokenAPIView',
)


class TeamViewSet(ListModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PeriodViewSet(ListModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer


class UserViewSet(ListModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilterSet


class ProfileViewSet(RetrieveModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_id='Get AuthToken',
    operation_description='인증정보를 사용해 사용자의 Token(key)과 User정보를 획득',
    responses={
        status.HTTP_200_OK: AuthTokenSerializer(),
    },
))
class AuthTokenAPIView(LoginView):
    def get_response_serializer(self):
        return AuthTokenSerializer
