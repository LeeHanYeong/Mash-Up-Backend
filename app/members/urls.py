from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import apis

router = SimpleRouter()
router.register('teams', apis.TeamViewSet)
router.register('periods', apis.PeriodViewSet)
router.register('users', apis.UserViewSet)
router.register('profile', apis.ProfileViewSet)

app_name = 'members'
urlpatterns = [
    path('auth-token/', apis.AuthTokenAPIView.as_view()),
    path('', include(router.urls)),
]
