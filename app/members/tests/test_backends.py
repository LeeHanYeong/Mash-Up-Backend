from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.utils.crypto import get_random_string
from model_bakery import baker

from members.backends import SettingsBackend, PhoneNumberBackend, EmailBackend
from members.models import User


class BackendTest(TestCase):
    def test_settings_backend(self):
        username = get_random_string(length=20)
        password = get_random_string(length=100)
        hashed = make_password(password)

        settings.ADMIN_USERNAME = username
        settings.ADMIN_PASSWORD = hashed

        user = authenticate(username=username, password=password)
        self.assertTrue(isinstance(user, User))

        no_user_identifier = authenticate(username=username + "1", password=password,)
        self.assertIsNone(no_user_identifier)

        no_user_password = authenticate(username=username, password=password + "1",)
        self.assertIsNone(no_user_password)

        # get_user확인
        self.assertTrue(self.client.login(username=username, password=password))
        self.client.logout()
        backend = SettingsBackend()
        self.assertIsNone(backend.get_user(user.pk + 1))

    def test_phone_number_backend(self):
        password = get_random_string(length=100)
        user = baker.make(User, phone_number="01044445555")
        user.set_password(password)
        user.save()

        user = authenticate(phone_number=user.phone_number, password=password,)
        self.assertTrue(isinstance(user, User))

        no_user_identifier = authenticate(
            phone_number="01033334444", password=password,
        )
        self.assertIsNone(no_user_identifier)

        no_user_password = authenticate(
            phone_number=user.phone_number, password=password + "1",
        )
        self.assertIsNone(no_user_password)

        # get_user확인
        self.assertTrue(
            self.client.login(phone_number=user.phone_number, password=password)
        )
        self.client.logout()
        backend = PhoneNumberBackend()
        self.assertIsNone(backend.get_user(user.pk + 1))

    def test_email_backend(self):
        password = get_random_string(length=100)
        email = "test@test.com"
        user = baker.make(User, email=email)
        user.set_password(password)
        user.save()

        user = authenticate(email=user.email, password=password)
        self.assertTrue(isinstance(user, User))

        no_user_identifier = authenticate(email="1" + user.email, password=password,)
        self.assertIsNone(no_user_identifier)

        no_user_password = authenticate(email=user.email, password=password + "1",)
        self.assertIsNone(no_user_password)

        # get_user확인
        self.assertTrue(self.client.login(email=user.email, password=password))
        self.client.logout()
        backend = EmailBackend()
        self.assertIsNone(backend.get_user(user.pk + 1))
