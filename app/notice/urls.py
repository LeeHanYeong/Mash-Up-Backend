from django.urls import path, re_path

from . import apis

app_name = 'notices'
urlpatterns = [
    path('', apis.NoticeListCreateAPIView.as_view()),
    path('<int:pk>/', apis.NoticeRetrieveUpdateDestroyAPIView.as_view()),
    re_path(r'attendances/(?:(?P<pk>\d+)/)?$', apis.AttendanceUpdateAPIView.as_view()),
]
