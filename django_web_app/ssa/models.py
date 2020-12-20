from random import shuffle, random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os

from users.models import Profile
from . import constants

class Game(models.Model):

    name = models.CharField(max_length=24, unique=True, null=True)
    state = models.CharField(max_length=24, default=constants.GAME_STATE_PENDING)
    users = models.ManyToManyField(User)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_owner')

    def start(self):
        users = list(self.users.all())
        player_count = len(users)
        state = self.state
        existing_players = list(self.get_players())

        if state == constants.GAME_STATE_PENDING and len(existing_players) == 0 and player_count >= self.get_min_players():
            players = []
            for user in users:
                players.append(Player(status=constants.ALIVE, game=self, profile=user))
            shuffle(players)
            for i in range(len(players)):
                p1 = players[i]
                if i == (len(players) - 1):
                    p2 = players[0]
                else:
                    p2 = players[i+1]
                p2.save()
                p1.target = p2
                p1.save()

            self.state = constants.GAME_STATE_ACTIVE
            self.save()
            return True

        return False

    def get_owner(self):
        return self.owner

    def get_players(self):
        return self.player_set.all()

    def get_user_count(self):
        users = self.users.all()
        if users is not None:
            return len(users)
        else:
            return 0

    def get_player_count(self):
        players = self.get_players()
        if players is not None:
            return len(players)
        else:
            return 0

    def get_min_players(self):
        return 3

    def get_active_player_count(self):
        players = self.get_players()
        count = 0
        if players is not None:
            for player in players:
                if player.status != constants.KILLED:
                    count += 1

        return count


    def __str__(self):
        name = self.name
        if name is None:
            name = str(self.id)
        return name

    def get_name(self):
        name = self.name
        if name is None or name == '':
            name = str(self.id)
        return name

    def get_state(self):
        state = self.state
        return state

    #add game log for who killed who

class Player(models.Model):
    status = models.CharField(max_length=24)
    target = models.ForeignKey('self', on_delete=models.CASCADE,null=True, blank=True)
    game = models.ForeignKey('Game', blank=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    known_assassin = models.ForeignKey('self',on_delete=models.SET(''), null=True, default='', blank=True, related_name='player_known_assassin')

    def set_known_assassin(self, player):
        self.known_assassin = player
        self.save()

    def knows_assassin(self):
        if self.get_target() is not None and self.get_target() == self.get_assassin():
            return True
        if self.known_assassin is not None and self.known_assassin != '':
            if self.known_assassin.status != constants.KILLED:
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
        elif status == constants.PENDING_REVERSE:
            badge_class = 'badge-warning'
        elif status == constants.WINNER:
            badge_class = 'badge-success'


        return badge_class

    def get_name(self):
        name = self.profile.profile.handle
        if name == '':
            name = self.profile.username
        return name

    def __str__(self):
        game = self.game
        name = self.get_name() + "(pk=" + str(self.id) + " game=" + str(game.id) + ")"
        return name

    def assassinate(self):
        self.status = constants.PENDING
        self.save()

    def reverse_assassinate(self):
        self.status = constants.PENDING_REVERSE
        self.save()

    def kill(self, killed_by: int):
        target = self.get_target()
        assassin = self.get_assassin()
        self.status = constants.KILLED
        self.target = None
        self.known_assassin = None
        self.save()

        if self.game.get_active_player_count() > 1:
            assassin.target = target
            assassin.save()
        else:
            winner = Player.objects.get(pk=killed_by)
            winner.win()
            winner.save()

    def test(self):
        josh = Player.objects.get(pk=8)
        micah = Player.objects.get(pk=9)

        josh.target = micah
        josh.revive()
        josh.save()

        micah.target = josh
        micah.revive()
        micah.save()

    def win(self):
        game = self.game
        game.state = constants.GAME_STATE_ENDED
        game.save()
        self.status = constants.WINNER
        self.save()

    def revive(self):
        self.status = constants.ALIVE
        self.save()

