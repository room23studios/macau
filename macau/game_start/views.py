from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from game_start.models import Game
from game_start.forms import NickForm, PinForm

import secrets

from . import jwt


def index(request):
    return HttpResponse("Hello, world")


def new_game(request):
    if request.method == 'POST':
        games = True
        while games:
            game_pin = secrets.randbelow(1000000)
            games = Game.objects.exclude(state="resolved").filter(pin=game_pin)

        game = Game(pin=game_pin)
        game.save()

        return HttpResponseRedirect('j/' + str(game_pin))
    else:
        return render(request, 'game_start/new_game.html')


def join_game_by_url(request, game_pin):
    game = Game.objects.filter(pin=game_pin, state="lobby").first()
    if game is None:
        # TODO: set a http code
        return HttpResponse("No game with this pin")

    # render form
    if request.method != 'POST':
        form = NickForm()
        context = {'pin': game_pin, 'form': form}
        return render(request, 'game_start/join.html', context=context)

    # handle POST
    form = NickForm(request.POST)
    if not form.is_valid():
        return HttpResponse("Invalid form")  # TODO: http code, errors

    payload = {
        "game_id": str(game.id),
        "nick": form.cleaned_data['nick']
    }
    token = jwt.sign(payload)

    # TODO: sign the token with JWT and send it to the template
    return render(request, 'game_start/game.html', context={"token": token})


def join_game_by_pin(request):
    if request.method != 'POST':
        form = PinForm()
        context = {'form': form}
        return render(request, 'game_start/pin.html', context=context)

    form = PinForm(request.POST)
    if not form.is_valid():
        return HttpResponse("Form invalid")  # TODO: http error code

    game_pin = form.cleaned_data['pin']
    return HttpResponseRedirect('j/' + str(game_pin))
