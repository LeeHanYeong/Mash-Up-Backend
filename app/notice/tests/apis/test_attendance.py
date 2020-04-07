from model_bakery import baker
from rest_framework.test import APITestCase

from members.models import User
from notice.models import Notice, Attendance


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
            path=f'/api/notices/attendances/{attendance.id}/',
            data={
                'vote': Attendance.VOTE_ATTEND,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('vote'), Attendance.VOTE_ATTEND)

        response = self.client.patch(
            path=f'/api/notices/attendances/',
            data={
                'notice_id': attendance.notice.id,
                'vote': Attendance.VOTE_LATE,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('vote'), Attendance.VOTE_LATE)
