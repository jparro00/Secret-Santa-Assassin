from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os

class Game(models.Model):

    def get_players(self):
        return self.player_set.all()

    def __str__(self):
        return str(self.id)

    #add game log for who killed who

class Player(models.Model):
    status = models.CharField(max_length=16)
    target = models.ForeignKey('self', on_delete=models.CASCADE,default=1, null=True, blank=True)
    game = models.ForeignKey('Game', blank=True, on_delete=models.CASCADE,default=1)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def get_name(self):
        name = self.profile.profile.handle
        if name is "":
            name = self.profile.username
        return name

    def __str__(self):
        return self.get_name()

    def kill(self, killed_by: int):
        self.status = 'Killed'
        self.save()

    def revive(self):
        self.status = 'Alive'
        self.save()

