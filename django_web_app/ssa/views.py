from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import Form, BaseForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView, TemplateView,
)

from . import constants
from .models import Game, Player
from .forms import JoinGame, TestForm
import operator
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve

from django.db.models import Q

from .templatetags.ssa_extras import get_player


class GameDetailView(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Game
    template_name = 'ssa/game.html'

class PlayerDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Game
    template_name = 'ssa/player.html'

    def get(self, request, pk):
        player = get_player(request.user, pk)
        target = player.target
        assassin = player.get_assassin()
        target = player
        assassin = player
        context = {
            'player': player,
            'target': target,
            'assassin': assassin,
            'constants': constants
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):

        game = Game.objects.get(pk=pk)
        user = request.user
        player = get_player(user, game)
        target = player.target
        assassin = player.get_assassin()

        if constants.FORM_ASSASSINATE in request.POST and target.status == constants.ALIVE:
            target.assassinate()
            target.save()
        elif constants.FORM_RETRACT_CLAIM in request.POST and target.status == constants.PENDING:
            target.revive()
            target.save()
        elif constants.FORM_REJECT_CLAIM in request.POST and player.status == constants.PENDING:
            player.known_assassin = player.get_assassin()
            player.revive()
            player.save()
        elif constants.FORM_CONFIRM_CLAIM in request.POST and player.status == constants.PENDING:
            player.kill(assassin.id)
            player.save()

        return redirect('player-detail', pk)


class HomeView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Game
    template_name = 'ssa/home.html'  # <app>/<model>_<viewtype>.html


def join(request):
    if request.method == "POST":
        # Get the posted form
        MyJoinForm = JoinGame(request.POST)

        if MyJoinForm.is_valid():
            game_id = MyJoinForm.cleaned_data['game_id']
            game = Game.objects.get(game_id)
    else:
        MyJoinForm = JoinGame()

    return render(request, 'ssa/game.html', {"game": game})

class MyGamesView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Game
    template_name = 'ssa/my-games.html'  # <app>/<model>_<viewtype>.html


class TestView(TemplateView):
    template_name = 'ssa/test.html'

    def get(self, request):
        #form = TestForm(initial={'text': 'valid'})
        form = TestForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TestForm(request.POST)
        text = "pre"
        if form.is_valid():
            text = form.cleaned_data['text']
        return HttpResponse(request.COOKIES)


