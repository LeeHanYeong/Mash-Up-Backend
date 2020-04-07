import os

from django.contrib import admin
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path, include

from .push import push_router
from .. import views, apis
from ..doc import RedocSchemaView

admin.site.site_header = 'Mash-Up 관리사이트'

urlpatterns_views = [
    path('', views.IndexView.as_view(), name='index'),
    path('push/', views.PushView.as_view(), name='push'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
urlpatterns_apis = [
    path('push/fcm/test/', apis.FCMTestAPIView.as_view()),
    path('push/', include(push_router.urls)),
    path('members/', include('members.urls')),
    path('notices/', include('notice.urls')),
]
urlpatterns = [
    path('doc/', RedocSchemaView.as_cached_view(cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('', include(urlpatterns_views)),
    path('api/', include(urlpatterns_apis)),
]

SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
if SETTINGS_MODULE in ('config.settings', 'config.settings.local', 'config.settings.dev'):
    try:
        import debug_toolbar

        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    except ModuleNotFoundError:
        pass
