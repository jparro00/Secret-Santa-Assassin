from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Game, Player
import operator
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve

from django.db.models import Q


class GameDetailView(DetailView):
    model = Game
    template_name = 'ssa/game.html'

class PlayerDetailView(DetailView):
    model = Game
    template_name = 'ssa/player.html'

