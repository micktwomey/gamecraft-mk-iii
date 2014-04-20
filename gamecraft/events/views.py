from django.shortcuts import render


def event_list(request):
    raise NotImplementedError("Write this :)")


def new_event(request):
    raise NotImplementedError("Write this :)")
    return render(request, 'gamecraft/index.html', {
        "events": range(10),
    })
