from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os
from . import constants

class Game(models.Model):

    def get_players(self):
        return self.player_set.all()

    def __str__(self):
        return str(self.id)

    #add game log for who killed who

class Player(models.Model):
    status = models.CharField(max_length=24)
    target = models.ForeignKey('self', on_delete=models.CASCADE,default=1, null=True, blank=True)
    game = models.ForeignKey('Game', blank=True, on_delete=models.CASCADE,default=1)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    known_assassin = models.ForeignKey('self',on_delete=models.SET(''), null=True, default='', blank=True, related_name='player_known_assassin')

    def knows_assassin(self):
        if self.known_assassin is not None and self.known_assassin is not '':
            if self.known_assassin.status is not constants.KILLED:
                return True
            else:
                self.known_assassin = None
                self.save()

        return False

    def get_target(self):
        target = self.target
        return target

    def get_assassin(self):
        try:
            assassin = Player.objects.get(target=self.id)
        except Player.DoesNotExist:
            assassin = None
        return assassin

    def get_badge_class(self):
        badge_class = ""
        status = self.status
        if status == constants.ALIVE:
            badge_class = 'badge-success'
        elif status == constants.PENDING:
            badge_class = 'badge-warning'
        elif status == constants.KILLED:
            badge_class = 'badge-danger'

        return badge_class

    def get_name(self):
        name = self.profile.profile.handle
        if name == '':
            name = self.profile.username
        return name

    def __str__(self):
        return self.get_name()

    def assassinate(self):
        self.status = constants.PENDING
        self.save()

    def kill(self, killed_by: int):
        target = self.get_target()
        assassin = self.get_assassin()
        self.status = constants.KILLED
        self.target = None
        self.known_assassin = None
        self.save()

        assassin.target = target
        assassin.save()

    def revive(self):
        self.status = 'Alive'
        self.save()

