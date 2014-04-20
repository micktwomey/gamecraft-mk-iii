from django.contrib import admin

from gamecraft.events.models import Event


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'starts'


admin.site.register(Event, EventAdmin)
