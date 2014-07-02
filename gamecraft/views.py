import mimetypes
import os

from django.core.files.storage import default_storage
import django.http
from django.shortcuts import render

from gamecraft.gamecrafts.models import (
    get_global_sponsorships,
    get_upcoming_gamecrafts,
)


def frontpage(request):
    return render(request, 'gamecraft/index.html', {
        "gamecrafts": get_upcoming_gamecrafts(),
        "global_sponsorships": get_global_sponsorships(),
    })


def codeofconduct(request):
    return render(request, "gamecraft/codeofconduct.html", {})


def get_media(request, path):
    if not default_storage.exists(path):
        raise django.http.Http404()

    fp = default_storage.open(path)
    content_type, _ = mimetypes.guess_type(os.path.basename(fp.filename))
    return django.http.HttpResponse(fp.read(), content_type=content_type)
