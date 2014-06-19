import datetime
import logging

import django.core.files.base
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

import pytz

import requests

LOG = logging.getLogger(__name__)
MODIFY_GAMECRAFT_PERMISSION = ("modify_gamecraft", "Can create, edit and delete a GameCraft")


class PublishedManager(models.Manager):
    """Filters by public events

    """
    def get_queryset(self):
        LOG.debug("Filtering with public=True")
        return super(models.Manager, self).get_queryset().filter(public=True)


class GameCraft(models.Model):
    """A GameCraft.

    Represents an upcoming event, a current event or previous event.
    """
    TIMEZONES = [(tz, tz) for tz in pytz.common_timezones]

    slug = models.SlugField(max_length=600, help_text="Short name in url, hopefully automatically populated :) e.g. 2014-04-03-london-gamecraft-2014")
    title = models.CharField(max_length=500, unique=True, help_text="Title of GC, e.g. 'London GameCraft 2014'")

    starts = models.DateTimeField(help_text="The extact time the GC starts, e.g. '2014-03-04 09:00'. This is used to control showing theme and mode of the event.")
    ends = models.DateTimeField(help_text="The time the GC ends. This is used to control the display of the event, it becomes and 'old' event at this point.")
    timezone = models.CharField(max_length=100, help_text="Time zone event is in.", choices=TIMEZONES, default="Europe/Dublin")

    location = models.CharField(max_length=1000, help_text="The address of the venue. E.g. DIT Kevin Street, Dublin 1. Something Google can figure out.")
    location_latitude = models.DecimalField(max_digits=9, decimal_places=7, blank=True, null=True, help_text="The latitude of the event for maps. Geocoded automatically or enter by hand as a fallback.")
    location_longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, help_text="The latitude of the event for maps. Geocoded automatically or enter by hand as a fallback.")

    header_background = models.ImageField(blank=True, help_text="The image used for the header background", upload_to="gamecraft/background/%Y/%m/%d")

    content = models.TextField(blank=True, help_text="The main event description, in Markdown. Currently also where you'd put ad hoc info like 'Hosted by...'.")
    theme = models.TextField(blank=True, help_text="The theme description, in Markdown. This is displayed after the event start.")
    judges = models.TextField(blank=True, help_text="Info on the judges, in Markdown. This might be handled specially to make it look fancy on the site.")

    public = models.BooleanField(default=False, help_text="Set to True to make visible generally, otherwise you need the specific link.")

    created = models.DateTimeField(auto_now_add=True, help_text="When this was created.")
    modified = models.DateTimeField(auto_now=True, help_text="When this was last modified.")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return "{self.title} - {self.starts:%Y-%m-%d}".format(self=self)

    class Meta:
        permissions = (
            MODIFY_GAMECRAFT_PERMISSION,
        )
        verbose_name = "GameCraft"
        ordering = ['-starts']

    def get_absolute_url(self):
        return reverse('view_gamecraft', kwargs={"slug": self.slug})

    def state(self):
        """Returns the current state of this gamecraft

        One of started, finished and upcoming
        """
        if self.started():
            return "started"
        if self.finished():
            return "finished"
        if self.upcoming():
            return "upcoming"

    def started(self):
        """Returns True if this gamecraft has started

        Means it's currently on right now, not finished or from the future.

        """
        now = timezone.now()
        LOG.debug("Is {} <= {} <= {}?".format(self.starts, now, self.ends))
        return self.starts <= now <= self.ends

    def finished(self):
        """Returns True if this gamecraft has finished

        """
        now = timezone.now()
        LOG.debug("Is {} >= {}?".format(now, self.ends))
        return now >= self.ends

    def upcoming(self):
        """Returns True if this gamecraft is from the future

        """
        now = timezone.now()
        LOG.debug("Is {} <= {}?".format(now, self.starts))
        return now <= self.starts

    def show_theme(self):
        """Returns True if the theme should be shown

        """
        return True if (self.started() or self.finished()) and self.theme else False

    def show_signup(self):
        """Returns True if the signup details should be shown

        """
        return self.upcoming()

    def published_news(self):
        return self.news.filter(public=True).filter(published__lte=timezone.now())


def get_upcoming_gamecrafts():
    """Returns a dict of all published upcoming gamecrafts (or current)

    Grouped by "started" and "upcoming".

    """
    gamecrafts = {}
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    LOG.debug("Filtering with now={!r}".format(now))
    for gc in GameCraft.published.filter(ends__gte=now).order_by("starts"):
        if gc.started():
            gamecrafts.setdefault("started", []).append(gc)
        else:
            gamecrafts.setdefault("upcoming", []).append(gc)
    return gamecrafts


class Sponsor(models.Model):
    """A GameCraft Sponsor

    Can be re-used across events and sponsorships.

    """
    created = models.DateTimeField(auto_now_add=True, help_text="When this was created.")
    modified = models.DateTimeField(auto_now=True, help_text="When this was last modified.")

    slug = models.SlugField(max_length=500, help_text="Short name of sponsor.")
    name = models.CharField(max_length=500, unique=True, help_text="Name of sponsor.")
    url = models.URLField(max_length=500, help_text="URL of sponsor's site.")

    logo_url = models.URLField(max_length=500, blank=True, null=True, help_text="URL to download logo from instead of direct upload.")
    logo = models.ImageField(blank=True, null=True, help_text="The image used for the sponsor logo", upload_to="gamecraft/sponsors/%Y/%m/%d")
    logo_thumbnail_medium = ImageSpecField(source='logo', processors=[ResizeToFit(300, 50)], format='PNG')
    logo_thumbnail_small = ImageSpecField(source='logo', processors=[ResizeToFit(100, 20)], format='PNG')

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            MODIFY_GAMECRAFT_PERMISSION,
        )
        ordering = ["name", "modified"]


def update_image_from_url(instance, url_attr, image_attr, save=False):
    """Fetches the image data from the url of the instance and sets it

    Used in conjunction with filepicker.io or a plain url

    Use save=True to trigger a save() on the instance.

    """
    url = getattr(instance, url_attr)
    if url:
        LOG.info("Fetching {} for {}".format(url, instance))
        response = requests.get(url)
        LOG.info("Fetched {} and got {}: {}".format(url, response, response.headers))
        if response.status_code == 200:
            filename = response.headers["X-File-Name"]
            LOG.info("Got filename {} for url {}".format(filename, url))
            image = getattr(instance, image_attr)
            image.save(filename, django.core.files.base.ContentFile(response.content), save=save)


SPONSORSHIP_LEVELS = (
    (10, "Platinum"),
    (20, "Gold"),
    (30, "Silver"),
    (40, "Indies"),
    # GOTO 10
)


class Sponsorship(models.Model):
    """A sponsorship (by a sponsor)

    Can be a set period of time or for a particular gamecraft

    """
    created = models.DateTimeField(auto_now_add=True, help_text="When this was created.")
    modified = models.DateTimeField(auto_now=True, help_text="When this was last modified.")

    sponsor = models.ForeignKey(Sponsor)

    description = models.TextField(blank=True, help_text="Optional blurb about this sponsorship (Markdown). Most likely won't get used yet :)")

    starts = models.DateTimeField(blank=True, null=True, help_text="The time the sponsorship starts.")
    ends = models.DateTimeField(blank=True, null=True, help_text="The time the sponsorship ends.")

    # Generates a get_level_display()
    level = models.IntegerField(blank=True, null=True, choices=SPONSORSHIP_LEVELS, help_text="Sponsorship level (if applicable)")

    gamecraft = models.ForeignKey(GameCraft, blank=True, null=True, on_delete=models.SET_NULL, help_text="If this is a single event sponsor then use this. Conflicts with starts and ends.")

    def __str__(self):
        return "{self.sponsor.name} {self.starts} {self.ends} {self.gamecraft}".format(self=self)

    class Meta:
        permissions = (
            MODIFY_GAMECRAFT_PERMISSION,
        )
        ordering = ['level', "-starts", "modified"]


def get_sponsorships_for_gamecraft(gamecraft):
    """Returns a dict of global and event sponsorships

    """
    return {
        "gamecraft": list(gamecraft.sponsorship_set.all()),
        "global": list(Sponsorship.objects.filter(
            starts__lte=gamecraft.ends,
            ends__gte=gamecraft.starts,
        ).all()),
    }


def get_global_sponsorships():
    now = timezone.now()
    return list(
        Sponsorship.objects.filter(
            starts__lte=now,
            ends__gte=now,
        ).all()
    )


class PublishedNewsManager(models.Manager):
    """Filters news by public and published date

    """
    def get_queryset(self):
        now = timezone.now()
        LOG.debug("Filtering with public=True and published <= {}".format(now))
        return super(models.Manager, self).get_queryset().filter(public=True).filter(published__lte=now)


class News(models.Model):
    """A news item

    Can relate to a particular gamecraft or be global

    """
    created = models.DateTimeField(auto_now_add=True, help_text="When this was created.")
    modified = models.DateTimeField(auto_now=True, help_text="When this was last modified.")
    published = models.DateTimeField(help_text="When to publish this (this can be in the future). Note that you'll need to tick the public flag too. This also controls the URL.")

    gamecraft = models.ForeignKey(GameCraft, blank=True, null=True, related_name="news", on_delete=models.SET_NULL, help_text="If this relates to a particular gamecraft use this.")

    slug = models.SlugField(max_length=600, help_text="Short name in url, hopefully automatically populated :) e.g. news-post")
    title = models.CharField(max_length=500, unique=True, help_text="Title of news post")

    content = models.TextField(blank=True, help_text="The news article, in Markdown.")

    public = models.BooleanField(default=False, help_text="Set to True to make visible generally, otherwise you need the specific link.")

    objects = models.Manager()
    published_objects = PublishedNewsManager()

    def __str__(self):
        return "{self.slug} ({self.gamecraft})".format(self=self)

    class Meta:
        permissions = (
            MODIFY_GAMECRAFT_PERMISSION,
        )
        verbose_name_plural = "news"
        ordering = ["published", "slug", "title", "modified", "created"]
        unique_together = ["published", "slug"]

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"slug": self.slug, "year": self.published.year, "month": self.published.month, "day": self.published.day})


class NewsNotFound(Exception):
    """Raised when news isn't found

    Typically you want to raise a django.http.Http404 at this point.

    """


def get_news(year, month, day, slug, public_only=False):
    """Retrieves a News object

    The combination of date + slug should be unique enough, otherwise an NewsNotFound exception is raised.

    """
    try:
        # Use midnight of the day after the date's day, to include all
        # times in that day and before.
        when = datetime.datetime(year, month, day, tzinfo=pytz.UTC) + datetime.timedelta(days=1)
        manager = News.published_objects if public_only else News.objects
        return manager.filter(published__lte=when).get(slug=slug)
    except (News.MultipleObjectsReturned, News.DoesNotExist) as e:
        raise NewsNotFound(e)
