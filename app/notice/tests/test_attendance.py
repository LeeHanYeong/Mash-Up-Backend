from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APITestCase

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
            baker.make(Attendance, user=user, notice=notice)
            for notice in notices
        ]
        attendance = attendances[0]
        attendance.vote = Attendance.VOTE_ATTEND
        attendance.save()

        qs = Notice.objects.with_count().with_voted(user=user)
        self.assertEqual(qs.filter(is_voted=True).count(), 1)
        self.assertEqual(qs.filter(is_voted=False).count(), 9)
        self.assertEqual(qs.get(is_voted=True).pk, attendance.notice.pk)


class AttendanceAPITest(APITestCase):
    def test_attendance_update(self):
        users = baker.make(User, _quantity=10)
        notice = baker.make(Notice, type=Notice.TYPE_ALL)
        attendances = [
            baker.make(Attendance, user=user, notice=notice)
            for user in users
        ]

        user = users[0]
        attendance = attendances[0]

        self.client.force_authenticate(user=user)
        response = self.client.patch(
            path=f'/api/notices/attendances/{attendance.pk}/',
            data={
                'vote': Attendance.VOTE_ATTEND,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('vote'), Attendance.VOTE_ATTEND)

        response = self.client.patch(
            path=f'/api/notices/attendances/',
            data={
                'notice_pk': attendance.notice.pk,
                'vote': Attendance.VOTE_LATE,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('vote'), Attendance.VOTE_LATE)
