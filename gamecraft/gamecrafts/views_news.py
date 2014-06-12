import logging

import django.http
from django.shortcuts import render

from gamecraft.gamecrafts import models

LOG = logging.getLogger(__name__)


def news_index(request):
    news = models.News.published_objects.all()
    return render(request, "gamecraft/news_index.html", {"all_news": news})


def view_news(request, year, month, day, slug):
    year, month, day = int(year), int(month), int(day)
    try:
        news = models.get_news(year, month, day, slug)
    except models.NewsNotFound:
        raise django.http.Http404()
    return render(request, "gamecraft/view_news.html", {"news": news})
