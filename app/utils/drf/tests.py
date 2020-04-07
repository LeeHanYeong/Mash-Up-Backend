from django.test import TestCase

from members.models import User
from utils.drf.exceptions import get_object_or_exception


class ExceptionTest(TestCase):
    def test_get_object_or_exception(self):
        with self.assertRaises(ValueError):
            get_object_or_exception(User, ValueError, pk=0)
