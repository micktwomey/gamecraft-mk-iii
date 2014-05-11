from django.contrib import admin

from gamecraft.gamecrafts.models import (
    Attachment,
    GameCraft,
)


class GameCraftAdmin(admin.ModelAdmin):
    exclude = []
    date_hierarchy = 'starts'
    list_display = ("slug", "title", "starts", "timezone", "public", "location", "created", "modified")
    list_filter = ("public",)
    search_fields = ("slug", "title", "location", "judges", "content", "theme")

admin.site.register(GameCraft, GameCraftAdmin)


class AttachmentAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ("comment", "created", "modified")
    search_fiels = ("comment",)

admin.site.register(Attachment, AttachmentAdmin)
