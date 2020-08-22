from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from push_notifications.gcm import GCMError
from push_notifications.models import GCMDevice
from rest_framework import generics, serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from utils.drf.exceptions import SendPushException

__all__ = (
    "PushTestSerializer",
    "FCMTestAPIView",
)


class PushTestSerializer(serializers.Serializer):
    registration_id = serializers.CharField()
    message = serializers.CharField()
    extra = serializers.DictField(required=False)

    class Meta:
        fields = (
            "registration_id",
            "message",
            "extra",
        )

    def _get_object(self):
        return GCMDevice.objects.get(
            registration_id=self.validated_data["registration_id"]
        )

    def validate_registration_id(self, value):
        if not GCMDevice.objects.filter(registration_id=value).exists():
            raise ValidationError("주어진 registration_id에 해당하는 GCM/FCM등록기기가 없습니다")
        return value

    def send_message(self):
        gcm_device = self._get_object()
        return gcm_device.send_message(
            message=self.validated_data.get("message", ""),
            extra=self.validated_data.get("extra", {}),
        )


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_summary="FCM Send Test",
        operation_description="FCM Push Test",
        responses={
            status.HTTP_200_OK: """
> FCM Send Result
```
{
    "multicastId": 7740128758730332408,
    "success": 0,
    "failure": 1,
    "canonicalIds": 0,
    "results": [
        {
            "error": "NotRegistered",
            "originalRegistrationId": "dGF7p38paUE:APA91bHN2nLXPD3VCID7qTbtbNhjRj0rAM-WvrJUvUvt5Cos7_aP1GvBW82_UPhYjx_LWYwwCeO5IgFtENC5zJJ0_OVxPc50aZwxPtQc0pF1osyk-zB795NCJPpBAwApDRtv3ZkJJnJ_"
        }
    ]
}
```
"""
        },
    ),
)
class FCMTestAPIView(generics.GenericAPIView):
    queryset = GCMDevice.objects.all()
    serializer_class = PushTestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = serializer.send_message()
            return Response(data)
        except GCMError as e:
            raise SendPushException(e.args)
