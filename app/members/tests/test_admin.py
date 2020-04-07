from django.test import TestCase
from model_bakery import baker
from rest_framework import status

from members.models import User, Team, Period, UserPeriodTeam, UserPeriodOutcount
from utils.test import get_admin_urls


class AdminTest(TestCase):
    def setUp(self) -> None:
        user = baker.make(User)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.user = user
        self.client.force_login(user=user)

    def test_200(self):
        for app, model in (
                ('members', User),
                ('members', Team),
                ('members', Period),
                ('members', UserPeriodTeam),
                ('members', UserPeriodOutcount),
        ):
            instance = baker.make(model)
            urls = get_admin_urls(f'admin:{app}_{model.__name__.lower()}', instance)
            for url in urls:
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
