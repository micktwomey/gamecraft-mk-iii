from django.test import TestCase


class SmokeTestEmptyDB(TestCase):
    def test_empty_views(self):
        for path, status in (
            ("/", 200),
            ("/events/fake-gamecraft/", 404),
            ("/events/", 200),
        ):
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, status)


class SmokeTestViews(TestCase):
    fixtures = ["gamecrafts"]

    def test_views(self):
        for path, status in (
            ("/", 200),
            ("/events/dublin-gamecraft-1/", 200),
            ("/events/dublin-gamecraft-ii/", 200),
            ("/events/fake-gamecraft/", 404),
            ("/events/", 200),
        ):
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, status)
