from django.test import TestCase
from model_bakery import baker

from notice.models import Notice
from utils.push.serializers import NoticePushSerializer


class SerializerTest(TestCase):
    def test_NoticePushSerializer(self):
        notice = baker.make(Notice, type=Notice.TYPE_ALL)
        serializer = NoticePushSerializer(notice)
        self.assertIsInstance(serializer.data, dict)
