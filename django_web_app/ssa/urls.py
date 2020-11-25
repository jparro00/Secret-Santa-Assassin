from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from .views import (
    GameDetailView, PlayerDetailView, HomeView, TestView
)
from . import views

urlpatterns = [
    #/ssa/
    path('', HomeView.as_view(), name='ssa-home'),
    path('game/<int:pk>/', GameDetailView.as_view(), name='game-detail'),
    path('<int:pk>', GameDetailView.as_view(), name='game-home'),
    path('my-game/<int:pk>', PlayerDetailView.as_view(), name='player-detail'),
    path('connection/', TemplateView.as_view(template_name='ssa/test.html')),
    url(r'^test/$', views.TestView.as_view(), name='test'),
    url(r'^my_games/$', views.MyGamesView.as_view(), name='my-games'),
]
