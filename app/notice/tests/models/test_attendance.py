from django.test import TestCase
from model_bakery import baker

from members.models import User
from notice.models import Notice, Attendance


class AttendanceModelTest(TestCase):
    def test_attendance_is_voted_annotate(self):
        """
        is_voted Annotation이 정상적으로 동작하는지 확인
        """
        user = baker.make(User)
        notices = baker.make(Notice, type=Notice.TYPE_ALL, _quantity=10)
        attendances = [
            baker.make(Attendance, user=user, notice=notice) for notice in notices
        ]
        attendance = attendances[0]
        attendance.vote = Attendance.VOTE_ATTEND
        attendance.save()

        qs = Notice.objects.with_count().with_voted(user=user)
        self.assertEqual(qs.filter(is_voted=True).count(), 1)
        self.assertEqual(qs.filter(is_voted=False).count(), 9)
        self.assertEqual(qs.get(is_voted=True).id, attendance.notice.id)
