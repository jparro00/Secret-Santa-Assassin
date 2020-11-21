from django.urls import path
from .views import (
    GameDetailView, PlayerDetailView
)
from . import views

urlpatterns = [
    path('game/<int:pk>/', GameDetailView.as_view(), name='game-detail'),
    path('<int:pk>', GameDetailView.as_view(), name='game-home'),
    path('player/<int:pk>', PlayerDetailView.as_view(), name='player-detail'),
]
