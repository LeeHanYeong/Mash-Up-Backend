from collections import OrderedDict
from typing import Type

from django.db import models
from django.utils.safestring import mark_safe
from drf_yasg import openapi
from drf_yasg.inspectors.field import get_basic_type_info
from phonenumber_field.serializerfields import PhoneNumberField as DefaultPhoneNumberField
from rest_framework import serializers

__all__ = (
    'PkModelField',
    'PhoneNumberField',
)


class PkModelFieldDoesNotExist(Exception):
    def __init__(self, model, id):
        self.model = model
        self.msg = '"{model_class}"에서 id={id}인 인스턴스를 찾을 수 없습니다'.format(
            model_class=model.__class__.__name__, id=id)

    def __str__(self):
        return self.msg


class PkModelFieldIsNotForRead(Exception):
    def __str__(self):
        return '"serializer"가 지정되지 않은 PkModelField는 생성시에만 사용할 수 있습니다'


class PkModelField(serializers.Field):
    """
    특정 Model의 instance를 나타내는 Field
    주어지는 데이터가
        dict
            {'id': 1} 또는 {'id': 1}
        literal (id가 될 수 있는 숫자/문자 등의 고정 값)
            1, '1'
    과 같은 여러 형태일 때 전부 처리해주도록 한다

    * 생성시에만 사용한다
    """

    def __init__(self, model: Type[models.Model],
                 serializer: Type[serializers.Serializer] = None,
                 *args, **kwargs):
        """
        :param model: Model class
        :param serializer: Serializer class to use in "to_representation"
        :param kwargs:
        """
        if not issubclass(model, models.Model):
            raise ValueError('PkModelField의 "model"인수에는 Django Model의 자식클래스가 전달되어야합니다')

        self.model = model
        self.pk_attname = model._meta.pk.attname
        self.serializer = serializer
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if not isinstance(data, self.model):
            if hasattr(data, 'get'):
                pk = data.get('id') or \
                     data.get('pk') or \
                     data.get(self.pk_attname, data)
            else:
                pk = data

            try:
                return self.model.objects.get(pk=pk)
            except self.model.DoesNotExist:
                raise PkModelFieldDoesNotExist(self.model, pk)
        return data

    def to_representation(self, value):
        if self.serializer:
            return self.serializer(value).data
        raise PkModelFieldIsNotForRead()

    @property
    def Meta(self):
        pk_field = self.model._meta.pk
        type_info = get_basic_type_info(pk_field)
        model_name = getattr(self.model._meta, 'verbose_name', self.model.__name__)
        properties = OrderedDict({
            self.pk_attname: openapi.Schema(
                type=type_info['type'],
            ),
            '<Other fields>': openapi.Schema(
                type=openapi.TYPE_STRING,
                description=mark_safe(
                    f'Other fields of the `{model_name}` object<br>'
                    f'(fields other than `{self.pk_attname}` do not affect API requests)'
                ),
            )
        })

        class _Meta:
            swagger_schema_fields = {
                'type': openapi.TYPE_OBJECT,
                'properties': properties,
                'title': f'{model_name} Object including "{self.pk_attname}" attribute',
            }

        return _Meta


class PhoneNumberField(DefaultPhoneNumberField):
    def to_representation(self, value):
        if hasattr(value, 'as_national'):
            return value.as_national
        return value
