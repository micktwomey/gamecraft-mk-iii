import datetime

from django.test import TestCase
from django.utils import timezone

import mock

import pytz

from gamecraft.gamecrafts import models


class GameCraftFixtureTestCase(TestCase):
    maxDiff = None
    fixtures = ["gamecrafts"]

    def test_finished_state(self):
        gc = models.GameCraft.objects.get(slug="dublin-gamecraft-1")
        self.assertEqual(gc.state(), "finished")
        self.assertFalse(gc.started())
        self.assertTrue(gc.finished())
        self.assertFalse(gc.upcoming())

    def test_show_theme(self):

        gc = models.GameCraft.objects.get(slug="dublin-gamecraft-1")
        self.assertNotEqual(gc.theme, "")
        self.assertTrue(gc.show_theme())

    def test_cork_gamecraft_now(self):
        """Problem with Cork GC showing up as finished

        Turns out it's end time was < start time :)
        """
        gc = models.GameCraft.objects.get(slug="cork-gamecraft-2014")
        with mock.patch("gamecraft.gamecrafts.models.timezone") as timezone:
            timezone.now.return_value = datetime.datetime(2014, 11, 22, 9, 0, 0, tzinfo=pytz.UTC)
            self.assertTrue(gc.upcoming())
            self.assertFalse(gc.started())
            self.assertFalse(gc.finished())
            self.assertEqual(gc.state(), "upcoming")

            timezone.now.return_value = datetime.datetime(2014, 11, 22, 10, 1, 0, tzinfo=pytz.UTC)
            self.assertFalse(gc.upcoming())
            self.assertTrue(gc.started())
            self.assertFalse(gc.finished())
            self.assertEqual(gc.state(), "started")


class GameCraftModelTestCase(TestCase):
    maxDiff = None

    def now(self):
        return timezone.now()

    def add_future_gamecraft(self):
        self.future_gamecraft = models.GameCraft(
            slug="from-the-future",
            title="From the Future",
            starts=self.now() + datetime.timedelta(days=1),
            ends=self.now() + datetime.timedelta(days=1, minutes=60),
            public=True,
        )
        self.future_gamecraft.save()
        return self.future_gamecraft

    def add_started_gamecraft(self):
        self.started_gamecraft = models.GameCraft(
            slug="from-the-present",
            title="From the Present",
            starts=self.now() - datetime.timedelta(minutes=60),
            ends=self.now() + datetime.timedelta(minutes=60),
            public=True,
        )
        self.started_gamecraft.save()
        return self.started_gamecraft

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

    def test_show_theme(self):

        self.add_started_gamecraft()
        self.assertEqual(self.started_gamecraft.theme, "")
        self.assertFalse(self.started_gamecraft.show_theme())
        self.started_gamecraft.theme = "A theme!"
        self.assertTrue(self.started_gamecraft.show_theme())

        self.add_future_gamecraft()
        self.assertEqual(self.future_gamecraft.theme, "")
        self.assertFalse(self.future_gamecraft.show_theme())
        self.future_gamecraft.theme = "A theme!"
        self.assertFalse(self.future_gamecraft.show_theme())


class SponsorshipTestCase(TestCase):
    def test_get_all_sponsorships_by_year(self):
        sponsor = models.Sponsor(
            slug="my-sponsor",
            name="My Sponsor",
            url="http://example.com/",
        )
        sponsor.save()

        sponsorships = []
        for (level, start, end, description) in (
            (10, datetime.datetime(2014, 1, 1, tzinfo=pytz.UTC), datetime.datetime(2015, 1, 1, tzinfo=pytz.UTC), "Platinum"),
            (20, datetime.datetime(2014, 1, 1, tzinfo=pytz.UTC), datetime.datetime(2015, 1, 1, tzinfo=pytz.UTC), "Gold"),
            (30, datetime.datetime(2014, 1, 1, tzinfo=pytz.UTC), datetime.datetime(2015, 1, 1, tzinfo=pytz.UTC), "Silver"),
            (40, datetime.datetime(2014, 1, 1, tzinfo=pytz.UTC), datetime.datetime(2015, 1, 1, tzinfo=pytz.UTC), "Indies"),
            (50, datetime.datetime(2014, 1, 1, tzinfo=pytz.UTC), datetime.datetime(2015, 1, 1, tzinfo=pytz.UTC), "Partner"),
            (60, datetime.datetime(2014, 1, 1, tzinfo=pytz.UTC), datetime.datetime(2015, 1, 1, tzinfo=pytz.UTC), "Media Partner"),
            (None, datetime.datetime(2014, 1, 1, tzinfo=pytz.UTC), datetime.datetime(2015, 1, 1, tzinfo=pytz.UTC), "None"),
        ):
            sponsorship = models.Sponsorship(
                starts=start,
                ends=end,
                sponsor=sponsor,
                level=level,
            )
            sponsorship.save()
            sponsorships.append(sponsorship)

        years = models.get_all_sponsorships_by_year()
        self.assertEqual(len(years), 1)

        year = years[0]
        self.assertEqual(year["year"], 2014)

        levels = [s.level for s in year["sponsorships"]]
        self.assertListEqual(levels, [10, 20, 30, 40, 50, 60, None])
