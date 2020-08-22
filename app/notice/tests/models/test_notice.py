from itertools import cycle

from django.test import TestCase
from model_bakery import baker

from members.models import User
from notice.models import Notice, Attendance


class NoticeQueryTest(TestCase):
    def test_annotate_vote(self):
        notice = baker.make(Notice, type=Notice.TYPE_ALL)
        users = baker.make(User, _quantity=10)
        attendances = baker.make(
            Attendance,
            notice=notice,
            user=cycle(users),
            vote=cycle([Attendance.VOTE_ATTEND, Attendance.VOTE_ABSENT]),
            _quantity=10,
        )
        self.assertEqual(Attendance.objects.count(), 10)
        user = users[0]
