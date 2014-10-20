import datetime

import pytz

from django.test import TestCase

from gamecraft.gamecrafts import models


class SmokeTestEmptyDB(TestCase):
    def test_empty_views(self):
        for path, status in (
            ("/", 200),
            ("/codeofconduct/", 200),
            ("/colophon/", 200),
            ("/events/", 200),
            ("/events/fake-gamecraft/", 404),
            ("/events/ical/", 200),
            ("/events/rss/", 200),
            ("/legal/", 302),
            ("/news/", 200),
            ("/news/2014/06/12/foo/", 404),
            ("/privacy/", 200),
            ("/thanks/", 200),
            ("/robots.txt", 200),
        ):
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, status)


class SmokeTestViews(TestCase):
    fixtures = ["gamecrafts"]

    def test_views(self):
        for path, status in (
            ("/", 200),
            ("/codeofconduct/", 200),
            ("/colophon/", 200),
            ("/events/", 200),
            ("/events/dublin-gamecraft-1/", 200),
            ("/events/dublin-gamecraft-ii/", 200),
            ("/events/fake-gamecraft/", 404),
            ("/events/ical/", 200),
            ("/events/rss/", 200),
            ("/legal/", 302),
            ("/news/", 200),
            ("/news/2014/06/12/foo/", 404),
            ("/privacy/", 200),
            ("/thanks/", 200),
            ("/robots.txt", 200),
        ):
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, status)

    def test_existing_gamecrafts(self):
        for gc in models.GameCraft.objects.all():
            resp = self.client.get("/events/{}/".format(gc.slug))
            self.assertEqual(resp.status_code, 200)
            self.assertIn(gc.title, resp.content.decode("UTF-8"))


class SmokeTestNews(TestCase):
    def setUp(self):
        self.fake_news = models.News(slug="fake-news", title="Fake News", published=datetime.datetime(2014, 6, 11, 14, 32, tzinfo=pytz.UTC), public=True)
        self.fake_news.save()

        self.private_news = models.News(slug="private-news", title="Private News", published=datetime.datetime(2014, 6, 11, 14, 32, tzinfo=pytz.UTC), public=False)
        self.private_news.save()

    def test_view_news(self):
        saved_news = models.News.objects.get(slug="fake-news")
        self.assertEqual(saved_news.id, self.fake_news.id)
        self.assertTrue(saved_news.public)

        saved_news = models.News.published_objects.get(slug="fake-news")
        self.assertEqual(saved_news.id, self.fake_news.id)

        saved_news = models.get_news(2014, 6, 11, "fake-news")
        self.assertEqual(saved_news.id, self.fake_news.id)

        response = self.client.get("/news/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.fake_news.title, response.content.decode("UTF-8"))
        self.assertNotIn(self.private_news.title, response.content.decode("UTF-8"))

        # Event though it's private it's viewable with a link
        response = self.client.get("/news/2014/06/11/private-news/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.private_news.title, response.content.decode("UTF-8"))

        response = self.client.get("/news/2014/06/11/fake-news/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.fake_news.title, response.content.decode("UTF-8"))
