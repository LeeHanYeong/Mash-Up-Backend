from django.test import TestCase


class DocTest(TestCase):
    def test_200(self):
        url = "/doc/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_openapi(self):
        url = "/doc/?format=openapi"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
