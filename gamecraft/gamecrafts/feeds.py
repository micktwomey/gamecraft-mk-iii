"""Feeds for GameCraft

"""

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from gamecraft.gamecrafts.models import GameCraft


class GameCraftRSSFeed(Feed):
    """GameCraft upcoming (and past) events feed

    """
    title = "Global GameCraft Events"
    description_template = "gamecraft/feeds/gamecraft.description.html"

    def link(self):
        return reverse("list_gamecrafts")

    def feed_url(self):
        return reverse("gamecraft_rss")

    def items(self):
        return GameCraft.published.all()[:10]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.created

    def item_updateddate(self, item):
        return item.modified
