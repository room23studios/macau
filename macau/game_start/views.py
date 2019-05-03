from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from . import redis_connection
from game_start.models import Game
from game_start.forms import NickForm, PinForm

import secrets


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
    if request.method == 'POST':
        form = NickForm(request.POST)
        if form.is_valid():
            games = Game.objects.filter(pin=game_pin, state="playing")
            if games:
                user_token = redis_connection.add_user(
                    form.cleaned_data['nick'], game_pin)
                context = {'pin': game_pin, 'user_token': user_token}
                return render(request, 'game_start/game.html', context=context)
            else:
                return HttpResponse("No game with this pin")
    else:
        form = NickForm()
        context = {'pin': game_pin, 'form': form}
        return render(request, 'game_start/join.html', context=context)


def join_game_by_pin(request):
    if request.method == 'POST':
        form = PinForm(request.POST)
        if form.is_valid():
            game_pin = form.cleaned_data['pin']
            games = Game.objects.exclude(state="resolved").filter(pin=game_pin)
            if not games:
                return HttpResponse("No game with this pin")
            elif not games.first().state == "lobby":
                return HttpResponse("Game already started")
            else:
                return HttpResponseRedirect('j/' + str(game_pin))
        else:
            return HttpResponse("Form invalid")

    else:
        form = PinForm()
        context = {'form': form}
        return render(request, 'game_start/pin.html', context=context)
