from django.contrib import admin

from gamecraft.gamecrafts.models import GameCraft


class GameCraftAdmin(admin.ModelAdmin):
    date_hierarchy = 'starts'
    list_display = ("slug", "title", "starts", "timezone", "public", "location", "created", "modified")
    list_filter = ("public",)
    search_fields = ("slug", "title", "location", "judges", "content", "theme")

admin.site.register(GameCraft, GameCraftAdmin)
