from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404 as drf_get_object_or_404
from rest_framework.views import exception_handler


def rest_exception_handler(exc, context):
    # Django의 ValidationError에 대응
    # if isinstance(exc, DjangoValidationError):
    #     if not settings.DEBUG:
    #         raise exc
    #     if hasattr(exc, 'message_dict'):
    #         exc = DRFValidationError(detail={'error': exc.message_dict})
    #     elif hasattr(exc, 'message'):
    #         exc = DRFValidationError(detail={'error': exc.message})
    #     elif hasattr(exc, 'messages'):
    #         exc = DRFValidationError(detail={'error': exc.messages})

    # 클라이언트에서 status및 code활용
    response = exception_handler(exc, context)
    if response:
        response.data['status'] = response.status_code
        # Exception에 'code'가 존재할 경우 해당 내용
        # 없으면 Response의 ErrorDetail이 가지고 있는 'code'값
        response.data['code'] = getattr(exc, 'code', getattr(exc, 'default_code', None)) or response.data['detail'].code
    return response


def get_object_or_exception(queryset, exception, *filter_args, **filter_kwargs):
    try:
        return drf_get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except Http404:
        raise exception


class SendPushException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = 'send_push_exception'
    default_detail = 'Push전송에 실패했습니다'
