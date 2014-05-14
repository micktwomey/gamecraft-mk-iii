from django.test import TestCase

from gamecraft.gamecrafts.models import GameCraft


class SmokeTestEmptyDB(TestCase):
    def test_empty_views(self):
        for path, status in (
            ("/", 200),
            ("/codeofconduct/", 200),
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
            ("/codeofconduct/", 200),
            ("/events/dublin-gamecraft-1/", 200),
            ("/events/dublin-gamecraft-ii/", 200),
            ("/events/fake-gamecraft/", 404),
            ("/events/", 200),
        ):
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, status)

    def test_existing_gamecrafts(self):
        for gc in GameCraft.objects.all():
            resp = self.client.get("/events/{}/".format(gc.slug))
            self.assertEqual(resp.status_code, 200)
            self.assertIn(gc.title, resp.content.decode("UTF-8"))
