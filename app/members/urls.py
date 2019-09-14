from django.urls import path

from . import apis

app_name = 'members'
urlpatterns = [
    path('', apis.UserListAPIView.as_view()),
    path('teams/', apis.TeamListAPIView.as_view()),
    path('periods/', apis.PeriodListAPIView.as_view()),
]
