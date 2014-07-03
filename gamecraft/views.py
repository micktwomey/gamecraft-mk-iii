import mimetypes
import os

from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
import django.http
from django.shortcuts import (
    redirect,
    render,
)

from gamecraft.gamecrafts.models import (
    get_all_sponsorships_by_year,
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


def thanks(request):
    return render(request, "gamecraft/thanks.html", {"sponsorship_years": get_all_sponsorships_by_year()})


def privacy(request):
    return render(request, "gamecraft/privacy.html", {})


def legal(request):
    return redirect(reverse("privacy"))


def colophon(request):
    return render(request, "gamecraft/colophon.html", {})


def get_media(request, path):
    if not default_storage.exists(path):
        raise django.http.Http404()

    fp = default_storage.open(path)
    content_type, _ = mimetypes.guess_type(os.path.basename(fp.filename))
    return django.http.HttpResponse(fp.read(), content_type=content_type)
