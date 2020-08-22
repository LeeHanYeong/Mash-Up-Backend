from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from push_notifications.api.rest_framework import (
    GCMDeviceAuthorizedViewSet,
    APNSDeviceAuthorizedViewSet,
)
from rest_framework.routers import SimpleRouter

__all__ = ("push_router",)


@method_decorator(
    name="retrieve", decorator=swagger_auto_schema(operation_summary="FCM Device Read")
)
@method_decorator(
    name="create", decorator=swagger_auto_schema(operation_summary="FCM Device Create")
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(operation_summary="FCM Device Update"),
)
@method_decorator(
    name="destroy", decorator=swagger_auto_schema(operation_summary="FCM Device Delete")
)
class GCMViewSet(GCMDeviceAuthorizedViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(auto_schema=None)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@method_decorator(
    name="retrieve", decorator=swagger_auto_schema(operation_summary="APNS Device Read")
)
@method_decorator(
    name="create", decorator=swagger_auto_schema(operation_summary="APNS Device Create")
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(operation_summary="APNS Device Update"),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_summary="APNS Device Delete"),
)
class APNSViewSet(APNSDeviceAuthorizedViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(auto_schema=None)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


push_router = SimpleRouter()
push_router.register("fcm", GCMViewSet)
push_router.register("apns", APNSViewSet)
