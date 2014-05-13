from django.shortcuts import render

from gamecraft.gamecrafts.models import get_upcoming_gamecrafts


def frontpage(request):
    return render(request, 'gamecraft/index.html', {
        "gamecrafts": get_upcoming_gamecrafts(),
    })


def codeofconduct(request):
    return render(request, "gamecraft/codeofconduct.html", {})
