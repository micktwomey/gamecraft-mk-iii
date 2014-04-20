from django.shortcuts import render


def frontpage(request):
    return render(request, 'gamecraft/index.html', {
        "events": range(10),
    })
