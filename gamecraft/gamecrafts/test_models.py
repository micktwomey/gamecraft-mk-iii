from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from gamecraft.gamecrafts import models


class GameCraftModelTestCase(TestCase):
    maxDiff = None
    fixtures = ["gamecrafts"]

    def now(self):
        return timezone.now()

    def add_future_gamecraft(self):
        self.future_gamecraft = models.GameCraft(
            slug="from-the-future",
            title="From the Future",
            starts=self.now() + timedelta(days=1),
            ends=self.now() + timedelta(days=1, minutes=60),
            public=True,
        )
        self.future_gamecraft.save()

    def add_started_gamecraft(self):
        self.started_gamecraft = models.GameCraft(
            slug="from-the-present",
            title="From the Present",
            starts=self.now() - timedelta(minutes=60),
            ends=self.now() + timedelta(minutes=60),
            public=True,
        )
        self.started_gamecraft.save()

    def test_get_upcoming_gamecrafts(self):
        self.add_started_gamecraft()
        self.add_future_gamecraft()
        gamecrafts = models.get_upcoming_gamecrafts()
        self.assertEquals([gc.slug for gc in gamecrafts["started"]], [self.started_gamecraft.slug])
        self.assertEquals([gc.slug for gc in gamecrafts["upcoming"]], [self.future_gamecraft.slug])

    def test_started_state(self):
        self.add_started_gamecraft()
        self.assertEqual(self.started_gamecraft.state(), "started")
        self.assertTrue(self.started_gamecraft.started())
        self.assertFalse(self.started_gamecraft.finished())
        self.assertFalse(self.started_gamecraft.upcoming())

    def test_future_state(self):
        self.add_future_gamecraft()
        self.assertEqual(self.future_gamecraft.state(), "upcoming")
        self.assertFalse(self.future_gamecraft.started())
        self.assertFalse(self.future_gamecraft.finished())
        self.assertTrue(self.future_gamecraft.upcoming())

    def test_finished_state(self):
        gc = models.GameCraft.objects.get(slug="dublin-gamecraft-1")
        self.assertEqual(gc.state(), "finished")
        self.assertFalse(gc.started())
        self.assertTrue(gc.finished())
        self.assertFalse(gc.upcoming())
