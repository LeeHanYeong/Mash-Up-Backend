import random

from django.test import TestCase
from model_bakery import baker

from members.models import Period, EmailValidation


class PeriodModelTest(TestCase):
    def test_period_save_update_is_current(self):
        for i in range(10):
            baker.make(Period, is_current=random.choice([True, False]))
        self.assertEqual(Period.objects.filter(is_current=True).count(), 1)


class EmailValidationModelTest(TestCase):
    def test_save(self):
        email_validation = baker.make(EmailValidation, code="")
        self.assertTrue(email_validation.code)
