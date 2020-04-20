from drf_writable_nested import WritableNestedModelSerializer as DefaultWritableNestedModelSerializer
from phonenumber_field.modelfields import PhoneNumberField as PhoneNumberModelField
from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer as DefaultModelSerializer

from utils.drf.fields import PhoneNumberField as PhoneNumberSerializerField

__all__ = (
    'ModelSerializerMixin',
    'ModelSerializer',
)


class ModelSerializerMixin:
    serializer_field_mapping = {
        **DefaultModelSerializer.serializer_field_mapping,
        PhoneNumberModelField: PhoneNumberSerializerField,
    }

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)


class ModelSerializer(ModelSerializerMixin, DefaultModelSerializer):
    pass


class WritableNestedModelSerializer(ModelSerializerMixin, DefaultWritableNestedModelSerializer):
    pass
