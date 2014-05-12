import logging

from django.contrib import admin

from gamecraft.gamecrafts.models import (
    GameCraft,
    Sponsor,
    Sponsorship,
    update_image_from_url,
)

LOG = logging.getLogger(__name__)


class GameCraftAdmin(admin.ModelAdmin):
    exclude = []
    date_hierarchy = 'starts'
    list_display = ("slug", "title", "starts", "timezone", "public", "location", "created", "modified")
    list_filter = ("public",)
    search_fields = ("slug", "title", "location", "judges", "content", "theme")

admin.site.register(GameCraft, GameCraftAdmin)


class SponsorAdmin(admin.ModelAdmin):
    exclude = []
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("slug", "name", "created", "modified")
    search_fiels = ("slug", "name", "url")

    def save_model(self, request, obj, form, change):
        update_image_from_url(obj, "logo_url", "logo")
        obj.save()

admin.site.register(Sponsor, SponsorAdmin)


class SponsorshipAdmin(admin.ModelAdmin):
    exclude = []
    date_hierarchy = 'starts'
    list_display = ("sponsor", "starts", "ends", "gamecraft", "created", "modified")

admin.site.register(Sponsorship, SponsorshipAdmin)
