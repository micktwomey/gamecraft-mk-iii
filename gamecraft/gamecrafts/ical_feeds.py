"""iCal Calendar feeds

"""

from gamecraft.django_ical.views import ICalFeed
from gamecraft.gamecrafts.models import GameCraft


class GameCraftICalFeed(ICalFeed):
    """GameCraft Event Calendar
    """

    product_id = '-//gamecraft.it//GameCraft//EN'
    timezone = 'UTC'

    def items(self):
        return GameCraft.published.all().order_by('-starts')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_start_datetime(self, item):
        return item.starts

    def item_end_datetime(self, item):
        return item.ends

    def item_location(self, item):
        return item.location

    def item_geolcoation(self, item):
        return (item.location_latitude, item.location_longitude)
