from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from .views import (
    GameDetailView, PlayerDetailView, MyGamesView, GameCreate, GameStatusView
)
from . import views

urlpatterns = [
    #/ssa/
    path('', MyGamesView.as_view(), name='ssa-home'),
    path('game/<int:pk>/', GameDetailView.as_view(), name='game-detail'),
    path('game/create/', GameCreate.as_view(), name='game-create'),
    path('<int:pk>', GameDetailView.as_view(), name='game-home'),
    path('my-game/<int:pk>', PlayerDetailView.as_view(), name='player-detail'),
    path('connection/', TemplateView.as_view(template_name='ssa/test.html')),
    path('test/<int:pk>/', views.TestView.as_view(), name='test'),
    url(r'^my-games/$', MyGamesView.as_view(), name='my-games'),
    path('game-status/<int:pk>/', GameStatusView.as_view(), name='game-status'),
]
