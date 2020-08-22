from rest_auth.views import LoginView
from rest_framework import permissions

from utils.drf.viewsets import ListModelViewSet, RetrieveModelViewSet
from .filters import UserFilterSet
from .models import Team, User, Period
from .serializers import (
    UserSerializer,
    TeamSerializer,
    PeriodSerializer,
    AuthTokenSerializer,
)

__all__ = (
    "TeamViewSet",
    "PeriodViewSet",
    "UserViewSet",
    "ProfileViewSet",
    "AuthTokenAPIView",
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


class AuthTokenAPIView(LoginView):
    def get_response_serializer(self):
        return AuthTokenSerializer
