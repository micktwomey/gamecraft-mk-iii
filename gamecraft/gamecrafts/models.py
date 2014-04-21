from django.core.urlresolvers import reverse
from django.db import models

import pytz


class PublishedManager(models.Manager):
    """Filters by public events

    """
    def get_queryset(self):
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

    header_background = models.FileField(blank=True, help_text="The image used for the header background")

    content = models.TextField(blank=True, help_text="The main event description, in Markdown. Currently also where you'd put ad hoc info like 'Hosted by...'.")
    theme = models.TextField(blank=True, help_text="The theme description, in Markdown. This is displayed after the event start.")
    judges = models.TextField(blank=True, help_text="Info on the judges, in Markdown. This might be handled specially to make it look fancy on the site.")

    public = models.BooleanField(default=False, help_text="Set to True to make visible generally, otherwise you need the specific link.")

    created = models.DateTimeField(auto_now_add=True, help_text="When this was created.")
    modified = models.DateTimeField(auto_now=True, help_text="When this was last modified.")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return "{self.title} {self.starts}".format(self=self)

    class Meta:
        permissions = (
            ("modify_gamecraft", "Can create, edit and delete a GameCraft"),
        )
        verbose_name = "GameCraft"

    def get_absolute_url(self):
        return reverse('view_gamecraft', kwargs={"slug": self.slug})
