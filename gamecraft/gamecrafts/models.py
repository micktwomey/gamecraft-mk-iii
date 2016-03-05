import datetime
import io
import logging
import mimetypes
import os.path

import boto

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from PIL import Image

import pytz

import requests

LOG = logging.getLogger(__name__)
MODIFY_GAMECRAFT_PERMISSION = ("modify_gamecraft", "Can create, edit and delete a GameCraft")

THUMBNAIL_MEDIUM_SIZE = (300, 50)
THUMBNAIL_SMALL_SIZE = (100, 20)


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
        # show theme 30 minutes after start, we never start on time :)
        started = (self.starts + datetime.timedelta(minutes=30)) <= timezone.now()
        return True if started and self.theme else False

    def show_signup(self):
        """Returns True if the signup details should be shown

        """
        return self.upcoming()

    def published_news(self):
        return self.news.filter(public=True).filter(published__lte=timezone.now())


def get_gamecrafts():
    """Get all gamecrafts grouped by state

    """
    gamecrafts = {}
    for gc in GameCraft.published.all().order_by("starts"):
        gamecrafts.setdefault(gc.state(), []).append(gc)
    return gamecrafts


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
    logo_public_url = models.URLField(max_length=500, blank=True, null=True, help_text="Public URL of the logo (for use in pages).")
    logo_thumbnail_medium_public_url = models.URLField(max_length=500, blank=True, null=True, help_text="Public URL of the medium sized logo (for use in pages).")
    logo_thumbnail_small_public_url = models.URLField(max_length=500, blank=True, null=True, help_text="Public URL of the medium sized logo (for use in pages).")

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            MODIFY_GAMECRAFT_PERMISSION,
        )
        ordering = ["name", "modified"]


def upload_to_s3_and_set_attr(bucket, instance, image_attr, subdir, filename, contents):
    url_format = "media/sponsors/{subdir}/{filename}"
    key = bucket.new_key(url_format.format(image_attr=image_attr, subdir=subdir, filename=filename))
    LOG.info("Uploading to {}".format(key))
    key.set_contents_from_string(contents, headers={'Content-Type': mimetypes.guess_type(filename)[0]}, policy='public-read')
    public_url = key.generate_url(0, "GET", query_auth=False)
    LOG.info("Setting public URL {}".format(public_url))
    setattr(instance, image_attr, public_url)


def update_image_from_url(instance, instance_name, url_attr, image_attr, save=False):
    """Fetches the image data from the url of the instance and sets it

    Used in conjunction with filepicker.io or a plain url

    Use save=True to trigger a save() on the instance.

    """
    LOG.info("Using access key {} and bucket {}".format(settings.AWS_ACCESS_KEY_ID, settings.IMAGES_S3_BUCKET))
    conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    LOG.info("Got S3 connection {}".format(conn))
    bucket = conn.get_bucket(settings.IMAGES_S3_BUCKET)
    LOG.info("Got S3 bucket {}".format(bucket))
    url = getattr(instance, url_attr)
    if url:
        LOG.info("Fetching {} for {}".format(url, instance))
        response = requests.get(url)
        LOG.info("Fetched {} and got {}: {}".format(url, response, response.headers))
        if response.status_code == 200:
            filename = response.headers["X-File-Name"]
            filename = os.path.join(instance_name, filename)
            LOG.info("Got filename {} for url {}".format(filename, url))

            # Upload image to S3 and store URL in image_attr + _public_url
            upload_to_s3_and_set_attr(bucket, instance, "{}_public_url".format(image_attr), "original", filename, response.content)

            for size, name in (
                (THUMBNAIL_MEDIUM_SIZE, "medium"),
                (THUMBNAIL_SMALL_SIZE, "small")
            ):
                prefix, _ = os.path.splitext(filename)
                thumbnail_filename = prefix + ".png"
                fp = io.BytesIO(response.content)
                fp.seek(0)
                im = Image.open(fp).convert("RGBA")
                im.thumbnail(size)
                out = io.BytesIO()
                im.save(out, "PNG")
                upload_to_s3_and_set_attr(bucket, instance, "{}_thumbnail_{}_public_url".format(image_attr, name), "thumbnail/{}".format(name), thumbnail_filename, out.getvalue())

            # Save image object
            instance.save()


SPONSORSHIP_LEVELS = (
    (10, "Platinum"),
    (20, "Gold"),
    (30, "Silver"),
    (40, "Indies"),
    (50, "Partner"),
    (60, "Media Partner"),
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
    sponsorships = {
        "gamecraft": [],
        "global": list(Sponsorship.objects.filter(
            starts__lte=gamecraft.ends,
            ends__gte=gamecraft.starts,
        ).all()),
    }
    sponsorships["gamecraft"] = [
        sponsorship for sponsorship in gamecraft.sponsorship_set.all()
        if sponsorship.sponsor not in [s.sponsor for s in sponsorships["global"]]
    ]
    return sponsorships


def get_global_sponsorships():
    now = timezone.now()
    return list(
        Sponsorship.objects.filter(
            starts__lte=now,
            ends__gte=now,
        ).all()
    )


def get_all_sponsorships_by_year():
    """Returns sponsorships by year

    """
    years = {}
    # extra ordering trick from http://stackoverflow.com/questions/7749216/django-order-by-date-but-have-none-at-end
    for sponsorship in (
            Sponsorship.objects.extra(
                select={
                    "level_is_null": "level IS NULL",
                    "starts_is_null": "starts IS NULL",
                }
            )
            .order_by("level_is_null", "level", "starts_is_null", "-starts", "-created", "-modified")
    ):
        if not sponsorship.starts:
            continue
        years.setdefault(sponsorship.starts.year, []).append(sponsorship)

    return [{"year": year, "sponsorships": sponsorships} for (year, sponsorships) in sorted(years.items(), reverse=True)]


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
        ordering = ["-published", "slug", "title", "-modified", "-created"]
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
