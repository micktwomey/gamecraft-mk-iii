import datetime
import logging
import uuid

from django.contrib.auth.decorators import permission_required
from django import forms
from django.http import HttpResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
import django.utils.timezone

from gamecraft.gamecrafts.models import (
    GameCraft,
    get_sponsorships_for_gamecraft,
)

LOG = logging.getLogger(__name__)


def list_gamecrafts(request):
    gamecrafts = GameCraft.published.all()
    return render(request, "gamecraft/gamecraft/index.html", {"gamecrafts": gamecrafts})


@permission_required('gamecrafts.modify_gamecraft')
def new_gamecraft(request):
    now = django.utils.timezone.now()
    start = now + datetime.timedelta(days=1)
    end = start + datetime.timedelta(days=1)
    gc = GameCraft(
        slug=str(uuid.uuid4()),
        title="New GameCraft {:%Y-%m-%d %H:%M}".format(start),
        starts=start,
        ends=end,
    )
    gc.save()
    return redirect('edit_gamecraft', slug=gc.slug)


class GameCraftForm(forms.ModelForm):
    class Meta:
        model = GameCraft
        exclude = []


@permission_required('gamecrafts.modify_gamecraft')
def edit_gamecraft(request, slug):
    gc = GameCraft.objects.get(slug=slug)
    if request.method == "POST":
        form = GameCraftForm(request.POST, instance=gc)
        if form.is_valid():
            form.save()
            redirect(gc)
    else:
        form = GameCraftForm(instance=gc)
    return render(request, "gamecraft/gamecraft/edit.html", {"gamecraft": gc, "form": form})


def view_gamecraft(request, slug):
    gc = get_object_or_404(GameCraft.objects, slug=slug)
    LOG.debug("Got GameCraft {}".format(gc))
    sponsorships = get_sponsorships_for_gamecraft(gc)
    LOG.debug("Got sponsorships {} for gamecraft {}".format(sponsorships, gc))
    return render(request, "gamecraft/gamecraft/view.html", {
        "gamecraft": gc,
        "global_sponsorships": sponsorships["global"],
        "gamecraft_sponsorships": sponsorships["gamecraft"],
    })


def view_background(request, slug):
    """As a fallback offer the background image

    """
    gc = get_object_or_404(GameCraft.objects, slug=slug)
    return HttpResponse(gc.header_background, content_type='image/png')
