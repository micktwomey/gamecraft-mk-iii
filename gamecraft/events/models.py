from django.db import models


class Event(models.Model):
    """A GameCraft Event.

    Represents an upcoming event, a current event or previous event.
    """
    slug = models.SlugField(max_length=600, help_text="Short name in url, hopefully automatically populated :) e.g. 2014-04-03-london-gamecraft-2014")
    title = models.CharField(max_length=500, unique=True, help_text="Title of GC, e.g. 'London GameCraft 2014'")

    starts = models.DateTimeField(help_text="The extact time the GC starts, e.g. '2014-03-04 09:00'. This is used to control showing theme and mode of the event.")
    ends = models.DateTimeField(help_text="The time the GC ends. This is used to control the display of the event, it becomes and 'old' event at this point.")

    location = models.CharField(max_length=1000, help_text="The address of the venue. E.g. DIT Kevin Street, Dublin 1. Something Google can figure out.")
    location_latitude = models.DecimalField(max_digits=9, decimal_places=7, blank=True, null=True, help_text="The latitude of the event for maps. Geocoded automatically or enter by hand as a fallback.")
    location_longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, help_text="The latitude of the event for maps. Geocoded automatically or enter by hand as a fallback.")

    header_background = models.FileField(blank=True, help_text="The image used for the header background")

    content = models.TextField(blank=True, help_text="The main event description, in Markdown. Currently where you'd put ad hoc info like 'Hosted by...' and Judges.")
    theme = models.TextField(blank=True, help_text="The theme description, in Markdown.")

    public = models.BooleanField(default=False, help_text="Set to True to make visible generally, otherwise you need the specific link.")

    def __str__(self):
        return "{self.title} {self.starts}".format(self=self)