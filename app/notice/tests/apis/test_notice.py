from copy import deepcopy
from datetime import datetime, timedelta

from dateutil.parser import isoparser, parse
from django.utils import timezone
from django.utils.crypto import get_random_string
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from members.models import User
from notice.models import Notice


class NoticeAPITest(APITestCase):
    URL_LIST = '/api/notices/'

    def _authenticate(self, user=None):
        if user is None:
            user = self.user
        self.client.force_authenticate(user=user)

    def setUp(self) -> None:
        self.user = baker.make(User)

    def test_notice_list_require_authenticate(self):
        response = self.client.get(self.URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_notice_list(self):
        self._authenticate()
        baker.make(Notice, type=Notice.TYPE_ALL, _quantity=100)
        response = self.client.get(self.URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 100)
        self.assertEqual(len(response.data['results']), 20)

    def test_notice_list_page(self):
        self._authenticate()
        page_size = 20
        page = 3
        notice_list = baker.make(Notice, type=Notice.TYPE_ALL, _quantity=100)
        query_params = {
            'page': page,
        }
        response = self.client.get(self.URL_LIST, query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 100)
        self.assertEqual(len(response.data['results']), page_size)
        self.assertListEqual(
            sorted([notice['id'] for notice in response.data['results']]),
            sorted([notice.id for notice in notice_list[page_size * 2:page_size * 3]]),
        )

    def test_notice_create_require_authenticate(self):
        response = self.client.post(self.URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_notice_create(self):
        notice_title = get_random_string()
        author = baker.make(User)
        start_at = timezone.make_aware(datetime(2020, 1, 1, 0, 0, 0))
        duration = timedelta(hours=4)
        address1 = get_random_string()
        address2 = get_random_string()
        description = get_random_string(200)

        user_list = baker.make(User, _quantity=20)

        data_obj = {
            'type': Notice.TYPE_ALL,
            'team': None,
            'title': notice_title,
            'author': {'id': author.id},
            'start_at': start_at,
            'duration': duration,
            'address1': address1,
            'address2': address2,
            'description': description,
            'user_set': [
                {'id': user.id} for user in user_list
            ]
        }
        data_list = deepcopy(data_obj)
        data_list['author'] = data_list['author']['id']
        data_list['user_set'] = [user['id'] for user in data_list['user_set']]

        self.client.force_authenticate(user=author)

        # 객체가 obj로 올 때와 id만 올 때 전부 테스트
        for data in (data_obj, data_list):
            response = self.client.post(self.URL_LIST, data=data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(data['type'], response.data['type'])
            self.assertEqual(data['title'], response.data['title'])
            self.assertEqual(data['start_at'], parse(response.data['start_at']))
            response_duration = datetime.strptime(response.data['duration'], '%H:%M:%S')
            self.assertEqual(
                data['duration'], timedelta(
                    hours=response_duration.hour,
                    minutes=response_duration.minute,
                    seconds=response_duration.second,
                )
            )
            self.assertEqual(data['address1'], response.data['address1'])
            self.assertEqual(data['address2'], response.data['address2'])
            self.assertEqual(data['description'], response.data['description'])
            self.assertEqual(len(response.data['attendance_set']), 20)
