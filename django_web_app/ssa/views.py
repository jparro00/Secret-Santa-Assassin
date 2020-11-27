
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView, TemplateView, FormView,
)

from . import constants
from .models import Game, Player
from .forms import JoinGame, TestForm, StartGameForm, AddForm, CreateGame
from django.urls import reverse_lazy, reverse
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
        elif constants.FORM_REVERSE_ASSASSINATE in request.POST and player.knows_assassin() and assassin.status == constants.ALIVE:
            assassin.reverse_assassinate()
            assassin.save()
        elif constants.FORM_RETRACT_CLAIM in request.POST and target.status == constants.PENDING:
            target.revive()
            target.save()
        elif constants.FORM_REJECT_CLAIM in request.POST and player.status == constants.PENDING:
            player.known_assassin = player.get_assassin()
            player.revive()
            player.save()
        elif constants.FORM_REJECT_REVERSE_CLAIM in request.POST and player.status == constants.PENDING_REVERSE:
            player.revive()
            player.save()
        elif constants.FORM_CONFIRM_CLAIM in request.POST and (player.status == constants.PENDING or player.status == constants.PENDING_REVERSE):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['constants'] = constants
        context['object_list'] = Game.objects.all()
        return context


    def post(self, request):

        form = StartGameForm(request.POST)
        user = request.user

        if form.is_valid() and request.user.is_authenticated:
            game_id = form.cleaned_data['game_id']
            game = Game.objects.get(pk=game_id)


        if constants.FORM_START_GAME in request.POST and game is not None and game.get_state() == constants.GAME_STATE_PENDING and user in game.users.all():
            game.start()

        return redirect('my-games')

class TestView(TemplateView):
    template_name = 'ssa/test.html'


    def get(self, request):
        form = AddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TestForm(request.POST)
        text = "pre"
        if form.is_valid():
            text = form.cleaned_data['text']
        return HttpResponse(request.COOKIES)


class CreateForm(object):
    pass


class GameCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Game
    form_class = CreateGame
    template_name = 'ssa/game_form.html'  # <app>/<model>_<viewtype>.html

    def get_success_url(self):
        return reverse('my-games')








