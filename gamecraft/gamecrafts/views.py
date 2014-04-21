import datetime
import uuid

from django.contrib.auth.decorators import permission_required
from django import forms
from django.shortcuts import (
    redirect,
    render,
)
import django.utils.timezone

from gamecraft.gamecrafts.models import GameCraft


def list_gamecrafts(request):
    raise NotImplementedError("Write this :)")


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
    return render(request, "gamecraft/edit_gamecraft.html", {"gamecraft": gc, "form": form})


def view_gamecraft(request, slug):
    gc = GameCraft.objects.get(slug=slug)
    return render(request, "gamecraft/view_gamecraft.html", {"gamecraft": gc})
