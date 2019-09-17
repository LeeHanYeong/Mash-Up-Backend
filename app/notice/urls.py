from django.urls import path

from . import apis

app_name = 'notices'
urlpatterns = [
    path('', apis.NoticeListCreateAPIView.as_view()),
    path('<int:pk>/', apis.NoticeRetrieveUpdateDestroyAPIView.as_view()),
    path('attendances/<int:pk>/', apis.AttendanceUpdateAPIView.as_view()),
]
