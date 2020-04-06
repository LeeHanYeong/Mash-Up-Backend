from typing import Tuple, Sequence

from django.utils.decorators import method_decorator
from drf_yasg.inspectors import SwaggerAutoSchema as DefaultSwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from inflection import camelize


class ResponseErrors(object):
    def __new__(cls, title, *errors):
        return cls.to_dict(title, *errors)

    @staticmethod
    def to_dict(title, *errors):
        return {
            title: {
                error.case: {
                    'code': error.code,
                    'message': error.message,
                } for error in errors
            }
        }


class SwaggerAutoSchema(DefaultSwaggerAutoSchema):
    def get_operation_id(self, operation_keys=None):
        operation_keys = operation_keys or self.operation_keys
        operation_id = self.overrides.get('operation_id', '')

        if not operation_id:
            if len(operation_keys) > 1:
                operation_keys = operation_keys[1:]

            operation_keys = [key[:-1] if key[-1] == 's' else key for key in operation_keys]
            operation_keys = [key.replace('-', '_') for key in operation_keys]
            operation_id = ' _'.join(operation_keys)
        return camelize(operation_id)


def schema(view, methods: Sequence[Tuple[str, dict]]):
    for method in methods:
        view = method_decorator(
            name=method[0], decorator=swagger_auto_schema(**method[1])
        )(view)
    return view
