from django.utils.crypto import get_random_string
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from members.models import User
from members.serializers import AuthTokenSerializer


class ProfileAPITest(APITestCase):
    URL = '/api/members/profile/'

    def test_require_authenticate(self):
        baker.make(User)
        url = self.URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api(self):
        user = baker.make(User)
        url = self.URL

        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthTokenAPITest(APITestCase):
    URL = '/api/members/auth-token/'

    def test_api(self):
        password = get_random_string(length=20)
        user = baker.make(User)
        user.set_password(password)
        user.save()

        data = {
            'username': user.username,
            'password': password,
        }
        response = self.client.post(self.URL, data, format='json')

        user = User.objects.get(pk=user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            AuthTokenSerializer(user.auth_token).data,
            response.data,
        )
