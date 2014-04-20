from django.contrib import admin

from gamecraft.gamecrafts.models import GameCraft


class GameCraftAdmin(admin.ModelAdmin):
    date_hierarchy = 'starts'


admin.site.register(GameCraft, GameCraftAdmin)
