from phonenumber_field.modelfields import PhoneNumberField as PhoneNumberModelField
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


class ModelSerializer(ModelSerializerMixin, DefaultModelSerializer):
    pass
