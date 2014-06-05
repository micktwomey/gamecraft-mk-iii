import logging

from django.contrib import admin

from imagekit.admin import AdminThumbnail

from gamecraft.gamecrafts import models

LOG = logging.getLogger(__name__)


class GameCraftAdmin(admin.ModelAdmin):
    exclude = []
    date_hierarchy = 'starts'
    list_display = ("slug", "title", "starts", "timezone", "public", "location", "created", "modified")
    list_filter = ("public",)
    search_fields = ("slug", "title", "location", "judges", "content", "theme")

admin.site.register(models.GameCraft, GameCraftAdmin)


class SponsorAdmin(admin.ModelAdmin):
    exclude = []
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("slug", "admin_thumbnail", "name", "created", "modified")
    search_fiels = ("slug", "name", "url")
    admin_thumbnail = AdminThumbnail(image_field='logo_thumbnail_small')

    def save_model(self, request, obj, form, change):
        models.update_image_from_url(obj, "logo_url", "logo")
        obj.save()

admin.site.register(models.Sponsor, SponsorAdmin)


class SponsorshipAdmin(admin.ModelAdmin):
    exclude = []
    date_hierarchy = 'starts'
    list_display = ("sponsor", "starts", "ends", "gamecraft", "created", "modified")

admin.site.register(models.Sponsorship, SponsorshipAdmin)


class NewsAdmin(admin.ModelAdmin):
    fields = ["title", "slug", "published", "gamecraft", "content", "public"]
    exclude = []
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published"
    list_display = ("title", "gamecraft", "published", "created", "modified", "public")
    list_filter = ("public",)
    search_fields = ("slug", "title", "content")
admin.site.register(models.News, NewsAdmin)
