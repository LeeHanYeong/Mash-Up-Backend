from rest_framework import status
from rest_framework.exceptions import APIException

__all__ = (
    'NoticeNotFound',
)


class NoticeNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'notice_not_found'
    default_detail = '해당 공지사항을 찾을 수 없습니다'
